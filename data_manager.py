import database_common
from psycopg2 import sql


@database_common.connection_handler
def get_mentor_names_by_first_name(cursor, first_name):
    cursor.execute("""
                    SELECT first_name, last_name FROM mentors
                    WHERE first_name = %(first_name)s ORDER BY first_name;
                   """,
                   {'first_name': first_name})
    names = cursor.fetchall()
    return names


@database_common.connection_handler
def get_all_applicants(cursor):
    cursor.execute("""
                    SELECT * FROM applicants;
                   """)
    applicants = cursor.fetchall()
    return applicants


@database_common.connection_handler
def get_all_mentors_data(cursor):
    cursor.execute("""
                    SELECT mentors.first_name, mentors.last_name, schools.name school_name, schools.country country
                    FROM mentors
                    INNER JOIN schools
                     ON mentors.city = schools.city
                    ORDER BY mentors.id;
                   """)
    names = cursor.fetchall()
    return names


@database_common.connection_handler
def get_all_school_data(cursor):
    cursor.execute("""
                     SELECT
                      COALESCE(mentors.first_name, 'No data') first_name,
                      COALESCE (mentors.last_name, 'No data') last_name,
                      schools.name school_name,
                      schools.country country
                     FROM mentors
                     RIGHT JOIN schools
                      ON mentors.city = schools.city
                     ORDER BY mentors.id;
                   """)
    school_data = cursor.fetchall()
    return school_data


@database_common.connection_handler
def get_number_of_mentors_by_country(cursor):
    cursor.execute("""
                    SELECT schools.country country, COUNT(*)
                    FROM mentors
                    INNER JOIN schools
                     ON mentors.city = schools.city
                    GROUP BY country
                    ORDER BY country;
                   """)
    number_of_mentors_by_country = cursor.fetchall()
    return number_of_mentors_by_country


@database_common.connection_handler
def get_applicants_and_mentors(cursor):
    cursor.execute("""
                    SELECT
                        applicants.first_name,
                        applicants.application_code,
                        COALESCE(mentors.first_name, 'No data'),
                        COALESCE(mentors.last_name, 'No data')
                    FROM applicants
                    LEFT JOIN applicants_mentors
                        ON applicants.id = applicants_mentors.applicant_id
                    LEFT JOIN mentors
                        ON mentors.id = applicants_mentors.mentor_id
                    ORDER BY applicants.id;
                   """)
    applicants_and_mentors = cursor.fetchall()
    return applicants_and_mentors


@database_common.connection_handler
def get_application_info(cursor):
    cursor.execute("""
                    SELECT 
                        applicants.first_name, 
                        applicants.application_code,
                        applicants_mentors.creation_date
                    FROM applicants
                    INNER JOIN applicants_mentors
                        ON applicants.id = applicants_mentors.applicant_id
                    WHERE creation_date > '2016-01-01'
                    ORDER BY creation_date DESC;
                   """)
    application_info = cursor.fetchall()
    return application_info


@database_common.connection_handler
def get_contacts(cursor):
    cursor.execute("""
                    SELECT schools.name school_name, mentors.first_name, mentors.last_name
                    FROM mentors
                    INNER JOIN schools
                     ON schools.contact_person = mentors.id
                    ORDER BY schools.name;
                   """)
    contacts = cursor.fetchall()
    return contacts


@database_common.connection_handler
def get_mentor_nicknames(cursor, city):
    cursor.execute("""
                    SELECT nick_name FROM mentors
                    WHERE city = %(city)s
                   """,
                   {'city': city})
    nicknames = cursor.fetchall()
    return nicknames


@database_common.connection_handler
def get_applicant_info(cursor, search_criterium, search_by_code=False):
    if search_by_code:
        cursor.execute("""
                        SELECT * FROM applicants
                        WHERE application_code = %(appl_code)s
                       """,
                       {'appl_code': search_criterium})

    else:
        cursor.execute("""
                                SELECT * FROM applicants
                                WHERE first_name = %(appl_name)s
                               """,
                       {'appl_name': search_criterium})

    applicant_info = cursor.fetchall()
    return applicant_info


@database_common.connection_handler
def get_applicant_info_by_email(cursor, email):
    pattern = f'%{email}%'
    cursor.execute("""
                    SELECT * FROM applicants
                    WHERE email LIKE %(email)s
                   """,
                   {'email': pattern})
    applicant_info = cursor.fetchall()
    return applicant_info


@database_common.connection_handler
def get_all_names_from_table(cursor, applicants=False):
    if applicants:
        cursor.execute("""
                        SELECT * FROM applicants
                       """)
    else:
        cursor.execute("""
                        SELECT * FROM mentors
                       """)
    names = cursor.fetchall()
    return names


@database_common.connection_handler
def append_to_database(cursor, table_name, user_input):
    cursor.execute(
        sql.SQL("""
                 INSERT INTO {table} (first_name, last_name, phone_number, email, application_code)
                 VALUES (%s, %s, %s, %s, %s)
                """)
            .format(table=sql.Identifier(table_name)),
        [user_input.get('first_name'),
         user_input.get('last_name'),
         user_input.get('phone_number'),
         user_input.get('email'),
         user_input.get('application_code')]
    )
