
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

        res = self.dpM.init_tables()
        self.assertEqual(res, 1)

    def test_insert_modify_delete(self):
        res = self.dpM.init_tables()

        #Insertion
        #res = 1
        line = ["","Micromod 30µm COOH","","","","","","","","20/6/2024","","","","","Arttu","Erkkobiomech 700189", 10001]
        res = self.dpM.insert_product(line)

        emp = Employee('Ilkka', 'tokki', 'doctoral researcher', 'Instru', '2020', '0504372337')
        res = self.dpM.insert_emp(emp)

        ##Modification
        res = self.dpM.update_emp("employees", "Arttu", "Lehtonen", "status", "fired")
        res = self.dpM.update_orders("orders", 10001, "Cas_No", "001")

        #Deletion
        res = self.dpM.remove_emp(emp)
        res = self.dpM.remove_product(10001)


        self.assertEqual(res, 1)



if __name__ == '__main__':
    unittest.main()