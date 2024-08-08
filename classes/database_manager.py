
import sqlite3 as sq

from tools.configs import properties_items

import numpy as np
import os
import csv


class DataBaseManager:
    
    def __init__(self, basepath, debug_flag):

        self.debug_flag = debug_flag
        self.download_path = "./bases/benchling_dump.csv"
        self.db_path = basepath

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
        
    def check_user(self, line):
        if len(line) != 9:
            print("user incorrect input")
            return -1
        bool_dummy = True
        bool_dummy *= len(line[0].split(" ") )== properties_items.user.len_name
        if not bool_dummy:
            print("Give first and last name separated by space ")
            return -1
        bool_dummy *= len(line[1]) > properties_items.user.len_password
        if not bool_dummy:
            print("Password needs to be over 8 characters long!")
            return -1
        bool_dummy *= len(line[6]) == properties_items.user.len_postal_code
        if not bool_dummy:
            print("Incorrect postal code")
            return -1
        bool_dummy *= len(line[2]) == properties_items.user.len_phone_number
        if not bool_dummy:
            print("Incorrecty phone number")
            return -1
        bool_dummy *= line[4] in properties_items.user.gender
        if not bool_dummy:
            print("Incorrect gender")
            return -1
        
        return 1


    def insert_user(self,line):
        ret = self.check_user(line)
        if ret == -1:
            return -1
        with self.conn:
            try:
                self.c.execute("""
                    INSERT INTO users (name, password, phone_number, age, gender, address, postal_code, postal_area, country)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, line)
                return 1
            except sq.Error as er:
                print("Cannot insert into users", er)
                return -1
            
    def update_user_record(self, target, record, value):
        with self.conn:
            try:
                self.c.execute("""UPDATE users SET {} = '{}'
                            WHERE name = '{}' """
                        .format( record, value, target))
                return 1
            except sq.Error as er:
                print(er)
                return -1

        
    def check_item(self, line):

        if len(line) != 12:
            print("item incorrect input")
            return -1
        
        bool_dummy = True
        bool_dummy *= line[0] in properties_items.info_items.TYPE_
        if not bool_dummy:
            print("Type needs to be", properties_items.info_items.TYPE_)
            return -1
        
        bool_dummy *= line[2] in properties_items.info_items.section
        if not bool_dummy:
            print("Description needs be some in", properties_items.info_items.section)
            return -1
        bool_dummy *= (line[5]>properties_items.info_items.price[0])*(line[5]<properties_items.info_items.price[1])
        if not bool_dummy:
            print("price needs to be over", properties_items.info_items.price[0] ,"and less than", properties_items.info_items.price[1])
            return -1
        bool_dummy *= len(line[7]) == properties_items.info_items.len_postal_code
        if not bool_dummy:
            print("Incorrect postal code")
            return -1
        bool_dummy *= line[8] in properties_items.info_items.condition
        if not bool_dummy:
            print("Incorrect gender")
            return -1
        
        return 1
    
    def insert_item(self, line): 

        ret = self.check_item(line)
        if ret == -1:
            return -1
        
        with self.conn:
            try:
                self.c.execute("""
                    INSERT INTO items (type, header, section, description, picture, price, product_ID, postal_code, condition, name, day_listed, day_sold)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, line)
                return 1
            except sq.Error as er:
                print("Cannot insert into items", er)
                return -1

    def update_item_record(self, target, record, value):
        with self.conn:
            try:
                self.c.execute("""UPDATE items SET {} = '{}'
                            WHERE product_ID = '{}'"""
                        .format( record, value, target))
                return 1
            except sq.Error as er:
                print(er)
                return -1
            
            
    def get_record(self, table, record, value):
        with self.conn:
            self.c.execute("SELECT * FROM {} WHERE {} = '{}'".format(table, record, value))
            return self.c.fetchone()
    

    def remove(self, table, value):
        with self.conn:
            try:
                if table == "items":
                    self.c.execute("DELETE from {} WHERE ID = '{}'".format(table, value))
                else:
                    self.c.execute("DELETE from {} WHERE ID = '{}'".format(table, value))
                return 1
            except sq.Error as er:
                print(er)
                return -1

    def get_all(self, table):
        try:
            with self.conn:
                self.c.execute("SELECT * FROM {}".format(table))
                print(self.c.fetchall())
        except sq.Error as er:
            print(er)
            return -1
        
    def print_table(self, table):
        with self.conn:
            self.c.execute("SELECT * FROM {}".format(table))
        
            return self.c.fetchall()

    def create_user_table(self):

        #make a table
        self.c.execute("""CREATE TABLE IF NOT EXISTS users (
                name text not null,
                password text, 
                phone_number text,
                age INTEGER,
                gender text,
                address text,
                postal_code text,
                postal_area text,
                country text,
                PRIMARY KEY (name)
                )""")
        
        self.commit()

    def create_item_table(self):

        self.c.execute("""CREATE TABLE IF NOT EXISTS items (
                type text,
                header text,
                section text,
                description text,
                picture BOOLEAN,
                price REAL,
                product_ID INTEGER,
                postal_code text,
                condition text,
                name text,
                day_listed text,
                day_sold text,
                PRIMARY KEY (product_ID),
                FOREIGN KEY (name) REFERENCES users(name)
                )""")
        
        self.commit()

    def init_tables(self):

        try:
            self.create_user_table()
        except sq.Error as er:
            print("user table creation failed", er)
            return -1 
        
        try:
            self.create_item_table() 
        except sq.Error as er:
            print("item teble creation failed", er)
            return -1 
        
        self.commit()
        return 1

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