#!/usr/bin/env python3

# Script: db.py
# Date: June, 16th, 2020
# Author: Piotr Kapela

# Description:
# Digital Bard DB interface is used to 
# abstract basic operations with SQLite.

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, Text, insert, select, delete, __version__

class DB:

    TABLE_NAME = "app_poems"
    
    def __init__(self):

        self.__engine = create_engine("sqlite:///vault.db", echo=True)
        self.__metadata = MetaData()

        if not self.__engine.dialect.has_table(self.__engine, DB.TABLE_NAME):

            connection = self.__engine.connect()
            
            app_poems = Table(DB.TABLE_NAME, self.__metadata,
                        Column("id", Integer, primary_key=True, autoincrement=True),
                        Column("poem", Text, nullable=False, default="No Poem")
            )

            self.__metadata.create_all(self.__engine)
            connection.close()
        
        return None
    
    def print_records(self):

        connection = self.__engine.connect()

        app_poems = Table(DB.TABLE_NAME, self.__metadata, autoload=True, autoload_with=self.__engine)
        stmt = select([app_poems])

        results = connection.execute(stmt).fetchall()
        for record in results:
            print(f"id: {record['id']}; poem: {record['poem']}")
        
        connection.close()

        return None
    
    def return_records(self):
        
        connection = self.__engine.connect()
        
        app_poems = Table(DB.TABLE_NAME, self.__metadata, autoload=True, autoload_with=self.__engine)
        stmt = select([app_poems])
        results = connection.execute(stmt).fetchall()

        connection.close()
        
        return results

    def insert_record(self, records_list):
        
        connection = self.__engine.connect()
        
        app_poems = Table(DB.TABLE_NAME, self.__metadata, autoload=True, autoload_with=self.__engine)
        stmt = insert(app_poems)
        result = connection.execute(stmt, records_list)
        
        connection.close()
        
        return result.inserted_primary_key
    
    def remove_record(self, record_index):
        
        connection = self.__engine.connect()
        
        #app_poems = self.__metadata.tables[DB.TABLE_NAME]
        app_poems = Table(DB.TABLE_NAME, self.__metadata, autoload=True, autoload_with=self.__engine)
        stmt = delete(app_poems).where(app_poems.c.id == record_index)
        connection.execute(stmt)

        connection.close()

        return None

    def get_version(self):
        
        print(f"SQLAlchemy ver. {__version__}")

        return None
