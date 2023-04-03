import aiohttp
import asyncio
import logging
from bs4 import BeautifulSoup
from typing import List

import constants
from data.dao import DAO
from helper import only_business_time
from telegram_channels import channels as ch


class Job:
    def __init__(self):
        self.dao = DAO.get_instance()

    @only_business_time
    def execute(self):
        try:
            jobs = asyncio.run(self.get_jobs())

            if jobs == None:  # couldn't get jobs
                return

            job_count = 0

            if not self.dao.exists:  # in the first execution, save the entire database
                job_history = self.parse_jobs(jobs)

                for job in job_history:
                    self.insert_db(job)
                    job_count += 1

                self.dao.exists = True

                logging.info("Database created and data was loaded successfully.")

            else:  # after being run for the first time, it will start sending alerts
                job_history = self.parse_jobs(jobs, constants.LIMIT_JOBS_PER_FETCH)

                for job in job_history:
                    if not self.exists_db(job):  # if the job is already registered, don't alert
                        self.insert_db(job)
                        job_count += 1

                        self.send_alert(job)

            return logging.info(f"{job_count} jobs inserted.")

        except Exception as e:
            logging.exception(e)
            return

    async def get_jobs(self) -> str:
        """makes a request to get jobs html"""

        for attempt in range(constants.MAX_ATTEMPTS):

            async with aiohttp.ClientSession() as ses:
                await ses.post(constants.LOGIN_URL, data=constants.USUARIO)
                jobs = await ses.get(constants.VAGAS_URL, data={"IdCurso": 4})

                if jobs.ok:
                    return await jobs.text()
                else:
                    logging.warn(
                        f"Attempt {attempt+1} failed (get_jobs() - code {jobs.status})"
                    )
                    await asyncio.sleep(constants.INTERVAL_MINUTES)

        else:
            logging.critical("Problems found when trying to get jobs")
            return None

    def parse_jobs(self, jobs, limit=None) -> List:
        """extracts information from html document"""

        parsed_html = BeautifulSoup(jobs, "html.parser")

        for strong_tag in parsed_html.find_all("strong"):
            strong_tag.extract()  # removes irrelevant strong tags

        if limit is not None:
            rows = parsed_html.find_all("div", class_="row")[: limit * 9]
        else:
            rows = parsed_html.find_all("div", class_="row")

        job_list = []

        for i in range(0, len(rows), 9):  # 1 job uses 9 "row" divs
            if i + 9 > len(rows):
                break

            job = rows[i : i + 9]

            job_details = {
                "DataCadastro": job[0].contents[1].text,
                "Empresa": job[1].contents[1].text,
                "Cargo": job[1].contents[3].text,
                "Tipo": job[2].contents[1].text,
                "Local": job[2].contents[3].text,
                "Requisitos": job[3].contents[1].text,
                "Beneficios": job[4].contents[1].text,
                "Description": job[5].contents[1].text,
                "Observacoes": job[6].contents[1].text,
            }
            self.format_job(job_details)

            job_list.append(job_details)

        return job_list

    def format_job(self, json: dict):
        for key, value in json.items():
            json[key] = value.replace("\n","").strip()
        
    def exists_db(self, job) -> bool:
        search = self.dao.jobs.search(
            # self.dao.query.CodigoVaga == job
            self.dao.query.fragment(job)
        )

        return len(search) > 0

    def send_alert(self, job: dict):
        message = "Nova vaga cadastrada:\n\n"
        for key, value in job.items():
            message += f"\n{value}\n"
        
        ch.send(constants.VAGAS_CHAT_ID, message)

    def insert_db(self, job) -> None:
        self.dao.jobs.insert(job)

    def update_db(self, job) -> None:
        self.dao.jobs.update(job)

    def delete_db(self, job) -> None:
        self.dao.jobs.remove(job)
