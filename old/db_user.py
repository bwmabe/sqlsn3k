import os
import sqlite3


class Prompt:
    prompt = "SQLSn3k %s> "

    def __init__(self, db, pwd):
        self.db = db
        self.pwd = pwd

    def __repr__(self):
        info_string = ""
        if self.pwd:
            info_string += f'{self.pwd}'
        if self.db:
            info_string += f'/{self.db}'
        return self.prompt % (info_string)

    def update(self, db, pwd=None):
        if pwd:
            self.pwd = pwd
        self.db = db


class DBUser():
    def __init__(self, to_connect=None):
        self.db = None
        self.db_name = None
        if to_connect:
            self.db = self.connect(to_connect)
            if self.db:
                self.db_name = to_connect.split('/')[-1]
        self.home = os.getenv("HOME")
        self.set_pwd()
        self.prompt = Prompt(self.db_name, self.pwd)

    def set_pwd(self):
        if self.home:
            self.pwd = os.getcwd().replace(self.home, '~')
        else:
            self.pwd = os.getcwd()

    def connect(self, path):
        try:
            return sqlite3.connect(path)
        except Exception as e:
            print(e)
            return None

    def disconnect(self):
        try:
            self.db.commit()
            self.db.close()
            self.db
        except Exception as e:
            print(e)

    def update(self):
        self.set_pwd()
        self.prompt.update(self.db_name, self.pwd)
