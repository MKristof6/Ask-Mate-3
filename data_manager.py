from typing import List, Dict
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
from psycopg2.extensions import AsIs
import connection

@connection.connection_handler
def get_answers(cursor: RealDictCursor, question_id) -> list:
    query = """
            SELECT *
            FROM answer
            WHERE question_id IN (%s)
            ORDER BY id 
            """
    cursor.execute(query, (question_id,))
    return cursor.fetchall()

@connection.connection_handler
def get_all_answers(cursor: RealDictCursor) -> list:
    query = """
            SELECT *
            FROM answer
            ORDER BY id """
    cursor.execute(query)
    return cursor.fetchall()

@connection.connection_handler
def get_question(cursor: RealDictCursor, question_id)-> list:
    query = """
               SELECT *
               FROM question
               WHERE id IN (%s)"""
    cursor.execute(query, (question_id,))
    return cursor.fetchall()

@connection.connection_handler
def get_last_question(cursor: RealDictCursor)-> list:
    query = """
               SELECT MAX(id)
               FROM question
                """
    cursor.execute(query)
    return cursor.fetchall()

@connection.connection_handler
def get_questions(cursor: RealDictCursor)-> list:
    query = """
               SELECT *
               FROM question
               ORDER BY id"""
    cursor.execute(query)
    return cursor.fetchall()

@connection.connection_handler
def write_answers(cursor: RealDictCursor, new_answer):
    query = """
            INSERT INTO answer (%s) VALUES (%s)
            """
    cursor.execute(query, (new_answer.keys(), new_answer.values()))

@connection.connection_handler
def write_question(cursor: RealDictCursor, question):
    query = """
                INSERT INTO question (id, submission_time, view_number, vote_number, title, message, image) 
                VALUES (%(id)s, date_trunc('seconds', localtimestamp), 
                %(view_number)s, %(vote_number)s, %(title)s, %(message)s, %(image)s);
                """
    cursor.execute(query, question)
    cursor.close()



