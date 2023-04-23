"""Data Access Layer"""

import logging
import os
import sys

from tinydb import TinyDB, Query
from tinydb.table import Table


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
            self._calculate_db_size()
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

    def _calculate_db_size(self):
        DAO.size = os.path.getsize(self.path)

    def insert_db(self, table, data) -> None:
        table.insert(data)
        self._calculate_db_size()

    def update_db(self, table, data) -> None:
        table.update(data)
        self._calculate_db_size()

    def delete_db(self, table, data) -> None:
        table.remove(data)
        self._calculate_db_size()

    def exists_db(self, table: Table, data: dict) -> bool:
        """
        Checks if a row already exists in the database

        Args:
            table (object): the table to search
            data (dict): the data to search

        Returns:
            bool: True if the row exists, False otherwise
        """

        search = table.search(self.query.fragment(
            data
        ))

        return len(search) > 0

    def contains_db(self, table: Table, query, aim_text: str) -> bool:
        """
        Checks if a row already exists in the database

        Args:
            table (object): the table to search
            aim_text (str): the text to search

        Returns:
            bool: True if the row exists, False otherwise
        """

        return table.contains(query == aim_text)

    def is_first_execution(self, table: Table):
        """
        Checks if the database is empty for an entity 
        or if it is the first execution

        Args:
            table (object): the table to search

        Returns:
            bool: True if the database is empty, False otherwise
        """
        
        if not self.created or self.size == 0 or len(table) == 0:
            return True

        return False