from flask import abort
from werkzeug.exceptions import NotFound

import data.database as database
from models.User import User
import psycopg2


class UsersDAO:
    def getUsers(self):
        connection = database.initialiseConnection()
        cursor = connection.cursor()
        sql = "SELECT * FROM projet.users"
        resultsExportUsers = []
        try:
            cursor.execute(sql)
            connection.commit()
            results = cursor.fetchall()

            for row in results:
                user = User(int(row[0]), str(row[1]), str(row[2]), str(row[3]), str(row[4]), str(row[5]),
                                 str(row[6]), str(row[7]))

                resultsExportUsers.append(user.convert_to_json())
            return resultsExportUsers
        except (Exception, psycopg2.DatabaseError) as e:
            try:
                print("SQL Error [%d]: %s" % (e.args[0], e.args[1]))
                raise Exception from e
            except IndexError:
                print("SQL Error: %s" % str(e))
                raise Exception from e
        finally:
            cursor.close()
            connection.close()

    def getUserById(self, id):
        connection = database.initialiseConnection()
        cursor = connection.cursor()
        sql = "SELECT id_user, lastname, firstname, email, pseudo, sexe, phone, password " \
              "FROM projet.users WHERE id_user = %i" % (id)
        try:
            cursor.execute(sql)
            connection.commit()
            result = cursor.fetchone()
            if result is None:
                abort(404, "User not found")
            user = User(result[0], result[1], result[2], result[3], result[4], result[5], result[6], result[7])
            return user
        except NotFound as not_found_e:
            raise not_found_e
        except (Exception, psycopg2.DatabaseError) as e:
            try:
                print("SQL Error [%d]: %s" % (e.args[0], e.args[1]))
                raise Exception from e
            except IndexError:
                print("SQL Error: %s" % str(e))
                raise Exception from e
        finally:
            cursor.close()
            connection.close()

    def singInUser(self, user):
        connection = database.initialiseConnection()
        cursor = connection.cursor()
        sql = "INSERT INTO projet.users VALUES (DEFAULT,'%s','%s','%s','%s','%s','%s','%s')" % (
            user['lastname'], user['firstname'], user['email'], user['pseudo'], user['sexe'], user['phone'],
            user['password'])
        try:
            cursor.execute(sql)
            connection.commit()
        except (Exception, psycopg2.DatabaseError) as e:
            try:
                print("SQL Error [%d]: %s" % (e.args[0], e.args[1]))
                raise Exception from e
            except IndexError:
                connection.rollback()
                print("SQL Error: %s" % str(e))
                raise Exception from e
        finally:
            cursor.close()
            connection.close()
