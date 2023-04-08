import requests
import logging
from bs4 import BeautifulSoup
from typing import List, Union
import time

import constants
from data.dao import DAO
from helper import only_business_time, make_request
from telegram_channels import channels, formatter


class Job:
    def __init__(self):
        self.dao = DAO.get_instance()
        self.execute()

    @only_business_time
    def execute(self):
        """
        Retrieves jobs, parses them, saves them to the database,
        and sends alerts when there are new job listings.

        Skips execution when off schedule (09h-20h).
        """

        logging.info("Fetching jobs...")
        start = time.time()

        try:
            jobs = self._get_jobs()

            if jobs is None:  # couldn't get jobs
                return

            job_count = 0

            if not self.dao.created or self.dao.size == 0:
                # in the first execution, save the entire database

                job_history = self._parse_jobs(jobs)

                for job in job_history:
                    self._insert_db(job)
                    job_count += 1

                self.dao.created = True
                logging.info("Database created and data was loaded successfully.")

            else:
                # after being run for the first time, it will start sending alerts

                job_history = self._parse_jobs(jobs, constants.LIMIT_JOBS_PER_FETCH)

                for job in list(reversed(job_history)):
                    # if the job is already registered, do not alert

                    if not self._exists_db(job):
                        self._insert_db(job)
                        job_count += 1

                        self._send_job_alert(job, True)

            end = time.time()
            elapsed_time = end - start

            self.dao.calculate_db_size()
            return logging.info(f"{job_count} jobs inserted ({elapsed_time:.2f}s).")

        except Exception as e:
            logging.error(e)

    def _get_jobs(self) -> Union[None, str]:
        """
        Retrieves job listings HTML from the website.

        Returns:
            str: Job listings HTML.
        """

        for attempt in range(constants.MAX_ATTEMPTS):
            with requests.Session() as ses:
                try:
                    make_request(constants.LOGIN_URL, "POST",
                        session=ses,
                        data=constants.USUARIO,
                    )

                    return make_request(constants.VAGAS_URL, "GET", 
                        session=ses, 
                        data={"IdCurso": 4}
                    ).text

                except Exception as e:
                    logging.error(f"An error occurred while making the request: {e}")
                    logging.warn(f"Attempt {attempt+1} failed (_get_jobs())")
                    time.sleep(constants.INTERVAL_MINUTES)

        else:
            logging.critical("Problems found when trying to fetch jobs")
            return None

    def _parse_jobs(self, jobs: str, limit=None) -> List[dict]:
        """
        Parses job listings HTML to extract relevant information.

        Args:
            `jobs` (str): Job listings HTML.
            `limit` (int, optional): Maximum number of jobs to retrieve. Defaults to None.

        Returns:
            List: List of dictionaries containing job details.
        """

        parsed_html = BeautifulSoup(jobs, "html.parser")

        _jobs_list = []
        _job = []
        _FILTER = ["Email:"]

        for row in parsed_html.find_all("div", class_="row"):
            if any(forbidden_row in row.text for forbidden_row in _FILTER):
                continue

            for inner_div in row.find_all("div"):
                if inner_div.text.replace("\n", "").strip():
                    for strong in inner_div.find_all("strong"):
                        strong.decompose()

                    _job.append(inner_div.text.replace("\n", "").strip())

            # TODO: validate if all fields of a job are filled,
            # else fill the unfilled with emtpy strings
            #
            # if all(_checks.values()):
            #     print("all filled")

            if len(_job) == 9:  # a single job requires 9 elements of information
                _jobs_list.append(_job.copy())
                _job.clear()

        final_result = self._format_jobs(
            _jobs_list[:limit] if limit is not None else _jobs_list
        )

        return final_result

    def _format_jobs(self, jobs: List) -> List[dict]:
        """
        Formats job details by transforming it in readable
        dictionaries and removing unnecessary characters.

        Args:
            `json` (list): Dictionary containing job details.
        """

        KEYS = constants.JOB_FIELDS.keys()

        _formatted_results = []

        for job in jobs:
            values = [detail.replace("\n", "").strip() for detail in job]
            _formatted_results.append(dict(zip(KEYS, values)))

        _formatted_results.reverse()  # 'order by date'

        return _formatted_results

    def _send_job_alert(self, job: dict, insert_emojis: bool = False) -> None:
        """
        Sends an alert for a new job listing.

        Args:
            `job` (dict): Dictionary containing job details.
            `insert_emojis` (bool): option to add emojis to the message
        """

        message = "Nova vaga cadastrada:\n\n"

        if insert_emojis:
            message = formatter.enhance(message, job)
        else:
            message += "\n".join(
                f"{key}: {value.capitalize()}" for key, value in job.items() if value
            )

        channels.send(constants.VAGAS_CHAT_ID, message)

    def _exists_db(self, job) -> bool:
        """checks if a job listing already exists in the database"""
        search = self.dao.jobs.search(self.dao.query.fragment(job))
        return len(search) > 0

    def _insert_db(self, job) -> None:
        self.dao.jobs.insert(job)

    def _update_db(self, job) -> None:
        self.dao.jobs.update(job)

    def _delete_db(self, job) -> None:
        self.dao.jobs.remove(job)
