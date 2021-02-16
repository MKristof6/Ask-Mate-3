from typing import List, Dict
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
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
def get_questions(cursor: RealDictCursor)-> list:
    query = """
               SELECT *
               FROM question
               ORDER BY id"""
    cursor.execute(query)
    return cursor.fetchall()

@connection.connection_handler
def write_answers(cursor: RealDictCursor, new_answer: str):
    query = """
            INSERT INTO answer (%s) VALUES (%s)
            """
    cursor.execute(query, (new_answer.keys() + new_answer.values()))

@connection.connection_handler
def write_question(cursor: RealDictCursor, new_question: str):
    query = """
                INSERT INTO question (%s) VALUES (%s)
                """
    cursor.execute(query, (new_question.keys() + new_question.values()))

