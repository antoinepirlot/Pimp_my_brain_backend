import psycopg2

import data.services.database as database
from data.services.DALService import DALService
from models.Course import Course


def _create_course_object(list_of_courses):
    """
    Creates a new list of Course. It transforms tuples in Course.
    :param: list_of_courses: list of tuples
    :return: a list of Course.
    """
    courses = []
    for course in list_of_courses:
        courses.append(Course(course[0], course[1], course[2], course[3], course[4], course[5], course[6]))
    return courses


class CoursesDAO:

    def __init__(self):
        self.dal = DALService()

    # __new__ Redefined to use singleton pattern
    def __new__(cls):
        if not hasattr(cls, "instance"):
            # No instance of CoursesDAO class, a new one is created
            cls.instance = super(CoursesDAO, cls).__new__(cls)
        # There's already an instance of CoursesDAO class, so the existing one is returned
        return cls.instance

    def get_one(self, id_course):
        """
        Get one course from the database
        :param id_course: the id of the requested course
        :return: the course matching with id_course. If there's no course, it returns None
        """
        sql = """
                SELECT id_category, id_teacher, course_description, price_per_hour, city, country, id_level           
                FROM projet.courses
                WHERE id_course = %(id_course)s;
              """
        values = {"id_course": id_course}
        self.dal.start()
        result = self.dal.commit(sql, values)
        if len(result) == 0:
            return None
        return _create_course_object(result)[0]

    def get_all_courses_from_teacher(self, id_teacher):
        """
        Get all teacher's courses from the database.
        :param id_teacher:  the teacher's id
        :return: the list of teacher's courses. If there's no courses, it returns None
        """
        sql = """
            SELECT DISTINCT id_category, id_teacher, course_description, price_per_hour, city, country, id_level
            FROM projet.courses
            WHERE id_teacher = %(id_teacher)s;
        """
        values = {"id_teacher": id_teacher}
        self.dal.start()
        result = self.dal.commit(sql, values)
        if len(result) == 0:
            return None
        return _create_course_object(result)

    def createOneCourse(self, course):
        connection = database.initialiseConnection()
        cursor = connection.cursor()
        sql = """
                INSERT INTO projet.courses (id_category, id_teacher, course_description, price_per_hour, city, country,
                id_level) VALUES( %(id_category)s, %(id_teacher)s, %(course_description)s, %(price_per_hour)s, %(city)s,
                %(country)s, %(id_level)s) RETURNING id_course
              """
        try:
            dico_variables = {"id_category": str(course.id_category), "id_teacher": str(course.id_teacher),
                              "course_description": course.course_description,
                              "price_per_hour": str(course.price_per_hour),
                              "city": course.city, "country": course.country, "id_level": str(course.id_level),
                              }
            cursor.execute(sql, dico_variables)
            connection.commit()
            results = cursor.fetchall()
            course.set_id_course(results[0][0])
            return course
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
