
import sqlite3 as sq
from classes.employee import Employee

import numpy as np
import os
import csv

class dataBaseManger_moc:

    def __init__(self) -> None:
        pass

    def call_random(self):

        return 1

class DataBaseManager:
    
    def __init__(self, basepath, table_flag, debug_flag):

        self.debug_flag = debug_flag
        self.download_path = "./bases/benchling_dump.csv"
        self.db_path = basepath

        ret = self.connect()

        if table_flag:
            ret = self.init_tables()

    def f(self, command):
        try:
            self.c.execute(command)
            return 1
        except sq.Error as er:
            print(er)
            return -1

    def connect(self):
        try:
            if not self.debug_flag:
                self.conn = sq.connect("bases/DataBase.db")
            else:
                self.conn = sq.connect(':memory:') #Everytime fresh database that runs on RAM
            #cursor
            self.c = self.conn.cursor()
            return 1
        except sq.Error as er:
            return er

    def check_user(self, cand):

    def insert_user(self,line):

        with self.conn:
            try:
                self.c.execute("""INSERT INTO users VALUES ( ? ? ? ? ? ? ? ? ? ? );""", line)
                return 1
            except sq.Error as er:
                print(er)
                return -1

    def check_item(self, cand):

    def insert_item(self, line): 

        with self.conn:
            try:
                self.c.execute("INSERT INTO items VALUES  ( ? ? ? ? ? ? ? ? ? ? ? ? );""", line)
                return 1
            except sq.Error as er:
                print(er)
                return -1

            
    def get_record(self, record, value, table):
        with self.conn:
            self.c.execute("SELECT * FROM {} WHERE {} = '{}'".format(table, record, value))
            return self.c.fetchone()
        

    def update_emp(self, table, first, last , record, value):
        with self.conn:
            try:
                self.c.execute("""UPDATE {} SET {} = '{}'
                            WHERE first = '{}' AND last = '{}'"""
                        .format(table, record, value, first, last))
                return 1
            except sq.Error as er:
                print(er)
                return -1
            
    def update_orders(self, table, idx , record, value):
        with self.conn:
            try:
                self.c.execute("""UPDATE {} SET {} = '{}'
                            WHERE idx = {} """
                        .format(table, record, value, idx))
                return 1
            except sq.Error as er:
                print(er)
                return -1

    def remove_emp(self, first, last):
        with self.conn:
            try:
                self.c.execute("DELETE from employees WHERE first = :first AND last = :last",
                        {'first': first, 'last': last})
                return 1
            except sq.Error as er:
                print(er)
                return -1
        
    def remove_product(self, idx):
        with self.conn:
            try:
                self.c.execute("DELETE from orders WHERE idx = {}".format(idx))
                return 1
            except sq.Error as er:
                print(er)
                return -1

    def get_posts(self, name):
        try:
            with self.conn:
                self.c.execute("SELECT * FROM {}".format(name))
                print(self.c.fetchall())
        except sq.Error as er:
            print(er)
            return -1
        
    def print_table(self, name):
        with self.conn:
            self.c.execute("SELECT * FROM {}".format(name))
        
            return self.c.fetchall()

    def create_user_table(self):

        #make a table
        self.c.execute("""CREATE TABLE IF NOT EXISTS users (
                name text not null,
                pasword text, 
                phone_number text,
                age int,
                gender str,
                address str,
                postal_code str,
                postal_area str,
                city str,
                country str,
                PRIMARY KEY (name)
                )""")
        
        self.commit()

    def create_product_table(self):

        self.c.execute("""CREATE TABLE IF NOT EXISTS items (
                type text,
                header text,
                section text,
                description int,
                picture bool,
                price real,
                product_ID	text,
                postal_code text,
                condition text,
                name text,
                day_listed text,
                day_sold text,
                PRIMARY KEY (product_ID),
                FOREIGN KEY (name) REFERENCES employees(name)
                )""")
        
        self.commit()

    def init_tables(self):

        try:
            self.create_employee_table()
            self.create_product_table() 

            self.commit()
            return 1
        except:
            print("table creation failed")
            return -1 

    def commit(self):
        self.conn.commit()

    def close(self):
        #close
        self.conn.close()


if __name__ == "__main__":
    print("No main defined")


"""
    with open(self.download_path, "r") as f:
        reader = csv.reader(f, delimiter=",")
        for i, line in enumerate(reader):
            if i == 0:
                continue
            
            line = [str(i or None) for i in line]

            for k, item in enumerate(line):
                if type(item) == "NoneType":
                    continue
            
            if line[-2] == "AL":
                line[-2] = "Arttu"
            elif line[-2] == "LS":
                line[-2] = "Linda"
            elif line[-2] == "MK":
                line[-2] = "Mari"
            elif line[-2] == "VM":
                line[-2] = "Vaino"
            
            line.extend([i])
            self.insert_product(line)
"""