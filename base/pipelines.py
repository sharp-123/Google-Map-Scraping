# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3


class BasePipeline(object):
    def __init__(self):
        self.create_connection()
        self.create_table()
    
    def create_connection(self):
        # Connect to the database
        self.conn = sqlite3.connect("Database.db")
        self.cursor = self.conn.cursor()

        # To create Table
        # self.cursor.execute("CREATE TABLE Data (id INTEGER PRIMARY KEY, Title TEXT, Reviews TEXT, Address TEXT, Monday TEXT, Tuesday TEXT, Wednesday TEXT, Thursday TEXT, Friday TEXT, Saturday TEXT, Sunday TEXT, Website TEXT, Phone TEXT, PlusCode TEXT)")
        # self.conn.commit()
        
    def create_table(self):
        self.cursor.execute('''DROP TABLE IF EXISTS Data''')
        self.cursor.execute("CREATE TABLE Data (id INTEGER PRIMARY KEY, Title TEXT, Reviews TEXT, Address TEXT, Monday TEXT, Tuesday TEXT, Wednesday TEXT, Thursday TEXT, Friday TEXT, Saturday TEXT, Sunday TEXT, Website TEXT, Phone TEXT, PlusCode TEXT)")
        self.conn.commit()

    def process_item(self, item, spider):
        self.store_db(item)
        return item
    
    def store_db(self, item):
        self.cursor.execute("INSERT INTO Data (Title, Reviews, Address, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, Website, Phone, PlusCode) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (
            item['Title'], item['Reviews'], item['Address'], item['Monday'], item['Tuesday'], item['Wednesday'], item['Thursday'], item['Friday'], item['Saturday'], item['Sunday'], item['Website'], item['Phone'], item['PlusCode']))
        self.conn.commit()