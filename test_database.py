
import unittest
from classes.database_manager import DataBaseManager
from classes.employee import Employee

import numpy as np
import os
import csv

class TestDatabase(unittest.TestCase):

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        
        self.dpM = DataBaseManager("./bases/DataBase", True)

    def test_connect(self):

        res = self.dpM.connect()
        self.assertEqual(res, 1)

    def test_create_tables(self):

        res = self.dpM.connect()
        res = self.dpM.init_tables()
        self.assertEqual(res, 1)

    def test_insert_modify_delete(self):

        res = self.dpM.connect()
        res = self.dpM.init_tables()
        #Insertion
        line = ["Matti Meikalainen", "123456728731", "0501231234", 10, "male", "jokutie 12C", "00110", "Helsinki", "Finland"]
        res = self.dpM.insert_user(line)


        line = ["sell" ,"header" ,"antique_and_art", "jotain", True ,100., 1, "00110" ,"new" ,"Matti Meikalainen", "01.01.2016" , "01.01.2015"] 
        res = self.dpM.insert_item(line)
        self.assertEqual(res, 1)
"""
        ##Modification
        res = self.dpM.update_emp("employees", "Arttu", "Lehtonen", "status", "fired")
        res = self.dpM.update_orders("orders", 10001, "Cas_No", "001")

        #Deletion
        res = self.dpM.remove_emp(emp)
        res = self.dpM.remove_product(10001)

"""


if __name__ == '__main__':
    unittest.main()
