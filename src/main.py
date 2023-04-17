import logging
import os
import schedule

from environment import production_environment
from helper import *
from models.jobs import Job
from models.menu import Menu
from models.news import News


def main():

    production_environment()

    _job = Job()
    _menu = Menu()

    def cardapio_job():
        _menu.fetch()

    def vagas_job():
        _job.execute()

    schedule.every(1).day.at(vm_localtime(17)).do(cardapio_job)
    schedule.every(2).hours.do(vagas_job)

    logging.info("Tasks scheduled")

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
