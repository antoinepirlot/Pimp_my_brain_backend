from requests import HTTPError
from data.services.DALService import DALService
from models.User import User

from flask import abort
from werkzeug.exceptions import NotFound

import data.database as database
import psycopg2


class UsersDAO:
    def __init__(self):
        self.dal = DALService()
        pass

    def get_users(self):
        sql = """SELECT * FROM projet.users"""
        resultsExportUsers = []

        results = self.dal.execute(sql, None, True)

        for row in results:
            user = User(int(row[0]), str(row[1]), str(row[2]), str(row[3]), str(row[4]), str(row[5]), str(row[6]),
                        str(row[7]))

            resultsExportUsers.append(user)
        return resultsExportUsers

    def get_user_by_id(self, id_user):
        sql = """SELECT id_user, lastname, firstname, email, pseudo, sexe, phone, password
                  FROM projet.users 
                  WHERE id_user = %(id_user)s;
                  """
        try:
            value = {"id_user": id_user}
            result = self.dal.execute(sql, value, True)
            if len(result) == 0:
                return None
            result = result[0]
            user = User(result[0], result[1], result[2], result[3], result[4], result[5], result[6], result[7])
            return user
        except Exception as e:
            raise e

    def get_user_by_email(self, email):
        sql = """SELECT id_user, lastname, firstname, email, pseudo, sexe, phone, password
                          FROM projet.users 
                          WHERE email = %(email)s;
                          """
        try:
            value = {"email": email}
            result = self.dal.execute(sql, value, True)
            if len(result) == 0:
                return None
            result = result[0]
            user = User(result[0], result[1], result[2], result[3], result[4], result[5], result[6], result[7])
            return user
        except Exception as e:
            raise e

    def get_user_by_pseudo(self, pseudo):
        sql = """SELECT id_user, lastname, firstname, email, pseudo, sexe, phone, password
                          FROM projet.users 
                          WHERE pseudo = %(pseudo)s;
                          """
        try:
            value = {"pseudo": pseudo}
            result = self.dal.execute(sql, value, True)
            if len(result) == 0:
                return None
            result = result[0]
            user = User(result[0], result[1], result[2], result[3], result[4], result[5], result[6], result[7])
            return user
        except Exception as e:
            raise e

    def sing_in_user(self, user):
        sql = "INSERT INTO projet.users VALUES (DEFAULT,'%s','%s','%s','%s','%s','%s','%s')" % (
            user['lastname'], user['firstname'], user['email'], user['pseudo'], user['sexe'], user['phone'],
            user['password'])
        try:
            self.dal.execute(sql, None)

        except (Exception, psycopg2.DatabaseError) as e:
            try:
                print("SQL Error [%d]: %s" % (e.args[0], e.args[1]))
                raise Exception from e
            except IndexError:
                print("SQL Error: %s" % str(e))
                raise Exception from e
