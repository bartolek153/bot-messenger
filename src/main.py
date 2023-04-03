import logging
import os
import schedule

from helper import *
from models.jobs import Job
from models.menu import Menu
from models.news import News


def main():
    """start point"""

    # os.environ["ENV"] = "development"  
    set_environment("production")

    _job = Job()
    _menu = Menu()
    # _news = News()

    def cardapio_job():
        _menu.execute()

    def vagas_job():
        _job.execute()

    # def noticias_job():
    #     _news.execute()

    schedule.every(1).day.at(vm_localtime(17)).do(cardapio_job)
    schedule.every(2).hours.do(vagas_job)
    # schedule.every(1).hour.do(noticias_job)

    logging.info("tasks scheduled")

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
