from typing import List, Dict
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
from psycopg2.extensions import AsIs
import connection

@connection.connection_handler
def get_answers_by_question_id(cursor: RealDictCursor, question_id) -> list:
    query = """
            SELECT *
            FROM answer
            WHERE question_id IN (%s)
            ORDER BY id 
            """
    cursor.execute(query, (question_id,))
    return cursor.fetchall()

@connection.connection_handler
def get_comments_by_question_id(cursor: RealDictCursor, question_id) -> list:
    query = """
            SELECT *
            FROM comment
            WHERE question_id IN (%s)
            ORDER BY id 
            """
    cursor.execute(query, (question_id,))
    return cursor.fetchall()

@connection.connection_handler
def get_answer_by_id(cursor: RealDictCursor, answer_id) -> list:
    query = """
            SELECT *
            FROM answer
            WHERE id IN (%s)
            """
    cursor.execute(query, (answer_id,))
    return cursor.fetchall()

@connection.connection_handler
def get_comment_by_id(cursor: RealDictCursor, comment_id) -> list:
    query = """
            SELECT *
            FROM comment
            WHERE id IN (%s)
            """
    cursor.execute(query, (comment_id,))
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
def get_all_comments(cursor: RealDictCursor) -> list:
    query = """
            SELECT *
            FROM comment
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
def get_last_few_questions(cursor: RealDictCursor)-> list:
    query = """
                   SELECT *
                   FROM question
                   ORDER BY id ASC
                   LIMIT 5;
                   """
    cursor.execute(query)
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
def get_last_answer(cursor: RealDictCursor)-> list:
    query = """
               SELECT MAX(id)
               FROM answer
                """
    cursor.execute(query)
    return cursor.fetchall()

@connection.connection_handler
def get_last_comment(cursor: RealDictCursor)-> list:
    query = """
               SELECT MAX(id)
               FROM comment
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
                    INSERT INTO answer (id, submission_time, vote_number, question_id, message, image) 
                    VALUES (%(id)s, date_trunc('seconds', localtimestamp), 
                    %(vote_number)s, %(question_id)s, %(message)s, %(image)s);
                    """
    cursor.execute(query, new_answer)
    cursor.close()

@connection.connection_handler
def write_comments(cursor: RealDictCursor, new_comment):
    query = """
                    INSERT INTO comment (id, question_id, answer_id, message, submission_time, edited_count) 
                    VALUES (%(id)s, %(question_id)s, %(answer_id)s, 
                    %(message)s, date_trunc('seconds', localtimestamp), 
                    %(edited_count)s);
                    """
    cursor.execute(query, new_comment)
    cursor.close()

@connection.connection_handler
def write_question(cursor: RealDictCursor, new_question):
    query = """
                INSERT INTO question (id, submission_time, view_number, vote_number, title, message, image) 
                VALUES (%(id)s, date_trunc('seconds', localtimestamp), 
                %(view_number)s, %(vote_number)s, %(title)s, %(message)s, %(image)s);
                """
    cursor.execute(query, new_question)
    cursor.close()

@connection.connection_handler
def delete_question(cursor: RealDictCursor, question_id):
    query = """
        DELETE FROM answer WHERE question_id IN (%s);
         DELETE FROM comment WHERE question_id IN (%s);
        DELETE FROM question  WHERE id IN (%s);
            """
    cursor.execute(query, (question_id, question_id, question_id))
    cursor.close()

@connection.connection_handler
def delete_answer(cursor: RealDictCursor, answer_id):
    query = """
        DELETE FROM answer WHERE id IN (%s);
            """
    cursor.execute(query, (answer_id,))
    cursor.close()

@connection.connection_handler
def delete_comment(cursor: RealDictCursor, comment_id):
    query = """
        DELETE FROM comment WHERE id IN (%s);
            """
    cursor.execute(query, (comment_id,))
    cursor.close()

@connection.connection_handler
def search_by_word(cursor: RealDictCursor, search: str)-> list:
    query = """
               SELECT *
               FROM question
               WHERE title LIKE %(key)s OR message LIKE %(key)s; """
    cursor.execute(query, {"key":  '%' + search + '%'})
    return cursor.fetchall()