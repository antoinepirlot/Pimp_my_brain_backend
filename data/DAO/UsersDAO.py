import psycopg2

from data.services.DALService import DALService
from models.User import User


class UsersDAO:
    def __init__(self):
        self.dal = DALService()

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

        value = {"id_user": id_user}
        result = self.dal.execute(sql, value, True)
        if len(result) == 0:
            return None
        result = result[0]
        user = User(result[0], result[1], result[2], result[3], result[4], result[5], result[6], result[7])
        return user

    def get_user_by_email(self, email):
        sql = """SELECT id_user, lastname, firstname, email, pseudo, sexe, phone, password
                          FROM projet.users 
                          WHERE email = %(email)s;
                          """

        value = {"email": email}
        result = self.dal.execute(sql, value, True)
        if len(result) == 0:
            return None
        result = result[0]
        user = User(result[0], result[1], result[2], result[3], result[4], result[5], result[6], result[7])
        return user

    def get_user_by_pseudo(self, pseudo):
        sql = """SELECT id_user, lastname, firstname, email, pseudo, sexe, phone, password
                              FROM projet.users 
                              WHERE pseudo = %(pseudo)s;
                              """

        value = {"pseudo": pseudo}
        result = self.dal.execute(sql, value, True)
        if len(result) == 0:
            return None
        result = result[0]
        user = User(result[0], result[1], result[2], result[3], result[4], result[5], result[6], result[7])
        return user

    def sing_in_user(self, user):
        sql = "INSERT INTO projet.users VALUES (DEFAULT,'%s','%s','%s','%s','%s','%s','%s')" % (
            user['lastname'], user['firstname'], user['email'], user['pseudo'], user['sexe'], user['phone'],
            user['password'])

        self.dal.execute(sql, None)
