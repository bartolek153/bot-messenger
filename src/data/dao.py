"""Data Access Layer"""

import logging
import os
import sys

from tinydb import TinyDB, Query


current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)


class DAO:
    _instance = None
    created = False
    size = 0

    @staticmethod
    def get_instance():
        """
        Gets the unique instance of data access object

        Returns:
            object: the object to read and write data to the database
        """
        if DAO._instance is None:
            DAO()

        return DAO._instance

    def __init__(self):
        self.path = os.path.join(parent_dir, "data", "db.json")

        if os.path.exists(self.path):
            DAO.created = True
            self.calculate_db_size()
        else:
            logging.info("Empty database created")

        self.db = TinyDB(self.path, sort_keys=True, indent=2, separators=(",", ":"))
        self.query = Query()

        self.jobs = self.db.table("Jobs")
        self.news = self.db.table("News")

        if DAO._instance is not None:
            raise Exception(
                "Data access object can't have more than one instance.")
        else:
            DAO._instance = self

    def calculate_db_size(self):
        DAO.size = os.path.getsize(self.path)

    def insert_db(self):
        pass

    def update_db(self):
        pass

    def delete_db(self):
        pass
