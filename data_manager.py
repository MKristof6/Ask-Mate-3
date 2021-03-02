from typing import List, Dict
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
from psycopg2.extensions import AsIs
import connection


@connection.connection_handler
def get_answers_by_question_id(cursor: RealDictCursor, question_id):
    query = """
        SELECT *
        FROM answer
        WHERE question_id IN (%s)
        ORDER BY id; 
        """
    cursor.execute(query, question_id)
    return cursor.fetchall()


@connection.connection_handler
def get_comments_by_question_id(cursor: RealDictCursor, question_id):
    query = """
        SELECT *
        FROM comment
        WHERE question_id IN (%s)
        ORDER BY id;
        """
    cursor.execute(query, question_id)
    return cursor.fetchall()


@connection.connection_handler
def get_answer_by_id(cursor: RealDictCursor, answer_id):
    query = """
        SELECT *
        FROM answer
        WHERE id IN (%s);
        """
    cursor.execute(query, (answer_id, ))
    return cursor.fetchall()


@connection.connection_handler
def get_comment_by_id(cursor: RealDictCursor, comment_id):
    query = """
        SELECT *
        FROM comment
        WHERE id IN (%s);
        """
    cursor.execute(query, (comment_id, ))
    return cursor.fetchall()


@connection.connection_handler
def get_all_answers(cursor: RealDictCursor):
    query = """
        SELECT *
        FROM answer
        ORDER BY id;
        """
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def get_all_comments(cursor: RealDictCursor):
    query = """
        SELECT *
        FROM comment
        ORDER BY id;
        """
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def get_question(cursor: RealDictCursor, question_id):
    query = """
        SELECT *
        FROM question
        WHERE id IN (%s);
        """
    cursor.execute(query, question_id)
    return cursor.fetchall()


@connection.connection_handler
def get_last_few_questions(cursor: RealDictCursor):
    query = """
        SELECT *
        FROM question
        WHERE id > (SELECT MAX(id) - 5 FROM question)
        ORDER BY id ASC;
        """
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def get_sorted_questions_asc(cursor: RealDictCursor, sort):
    cursor.execute(
        sql.SQL("SELECT * FROM {table} ORDER BY {col} {direction} LIMIT 5 ").format(col=sql.Identifier(sort),
                                                                                    table=sql.Identifier('question'),
                                                                                    direction=sql.SQL('ASC')))
    return cursor.fetchall()


@connection.connection_handler
def get_sorted_questions_desc(cursor: RealDictCursor, sort):
    cursor.execute(
        sql.SQL("SELECT * FROM {table} ORDER BY {col} {direction} LIMIT 5 ").format(col=sql.Identifier(sort),
                                                                                    table=sql.Identifier('question'),
                                                                                    direction=sql.SQL('DESC')))
    return cursor.fetchall()


@connection.connection_handler
def get_questions(cursor: RealDictCursor) -> list:
    query = """
       SELECT *
       FROM question
       ORDER BY id;
       """
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def write_answers(cursor: RealDictCursor, new_answer):
    query = """
        INSERT INTO answer (submission_time, vote_number, question_id, message, image) 
        VALUES (date_trunc('seconds', localtimestamp), %(vote_number)s, %(question_id)s, %(message)s, %(image)s);
        """
    cursor.execute(query, new_answer)
    cursor.close()


@connection.connection_handler
def write_comments(cursor: RealDictCursor, new_comment):
    query = """
        INSERT INTO comment (question_id, answer_id, message, submission_time, edited_count) 
        VALUES (%(question_id)s, %(answer_id)s, %(message)s, date_trunc('seconds', localtimestamp), %(edited_count)s);
        """
    cursor.execute(query, new_comment)
    cursor.close()


@connection.connection_handler
def write_question(cursor: RealDictCursor, new_question):
    query = """
        INSERT INTO question (submission_time, view_number, vote_number, title, message, image) 
        VALUES (date_trunc('seconds', localtimestamp), %(view_number)s, %(vote_number)s, 
        %(title)s, %(message)s, %(image)s);
        """
    cursor.execute(query, new_question)
    cursor.close()


@connection.connection_handler
def edit_question(cursor: RealDictCursor, new_question):
    query = """
        UPDATE question 
        SET id= %(id)s, submission_time = date_trunc('seconds', localtimestamp), view_number= %(view_number)s, 
        vote_number= %(vote_number)s, title=%(title)s, message=%(message)s, image=%(image)s
        WHERE id IN (%(id)s);
        """
    cursor.execute(query, new_question)
    cursor.close()


@connection.connection_handler
def delete_question(cursor: RealDictCursor, question_id):
    query = """
        DELETE FROM comment WHERE answer_id IN (%s);
        DELETE FROM answer WHERE question_id IN (%s);
        DELETE FROM comment WHERE question_id IN (%s);
        DELETE FROM question_tag WHERE question_id IN (%s);
        DELETE FROM question WHERE id IN (%s); 
        """
    cursor.execute(query, (question_id, question_id, question_id, question_id, question_id))
    cursor.close()


@connection.connection_handler
def delete_answer(cursor: RealDictCursor, answer_id):
    query = """
        DELETE FROM comment WHERE answer_id IN (%s);
        DELETE FROM answer WHERE id IN (%s);
        """
    cursor.execute(query, (answer_id, answer_id))
    cursor.close()


@connection.connection_handler
def delete_comment(cursor: RealDictCursor, comment_id):
    query = """
        DELETE FROM comment WHERE id IN (%s);
        """
    cursor.execute(query, (comment_id, ))
    cursor.close()


# @connection.connection_handler
# def delete_comment_by_question_id(cursor: RealDictCursor, question_id):
#     query = """
#         DELETE FROM comment WHERE question_id IN (%s);
#         """
#     cursor.execute(query, question_id)
#     cursor.close()
#
#
# @connection.connection_handler
# def delete_comment_by_answer_id(cursor: RealDictCursor, answer_id):
#     query = """
#         DELETE FROM comment WHERE answer_id IN (%s);
#         """
#     cursor.execute(query, answer_id)
#     cursor.close()


@connection.connection_handler
def search_by_word(cursor: RealDictCursor, search):
    query = """
        SELECT *
        FROM question
        WHERE title LIKE %(key)s OR message LIKE %(key)s;
        """
    cursor.execute(query, {"key": '%' + search + '%'})
    return cursor.fetchall()


@connection.connection_handler
def get_tag_by_question_id(cursor: RealDictCursor, question_id):
    query = """
        SELECT tag_id
        FROM question_tag
        where question_id IN (%s);
        """
    cursor.execute(query, question_id)
    return cursor.fetchall()


@connection.connection_handler
def get_tag_by_id(cursor: RealDictCursor, tag_id):
    query = """
        SELECT *
        FROM tag
        where id IN (%s);
        """
    cursor.execute(query, tag_id)
    return cursor.fetchall()


@connection.connection_handler
def get_last_tag(cursor: RealDictCursor):
    query = """
        SELECT MAX(id)
        FROM tag;
        """
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def add_new_tag(cursor: RealDictCursor, tags):
    query = """
        INSERT INTO tag (id, name) 
        VALUES (%(id)s, %(name)s);
        """
    cursor.execute(query, tags)
    cursor.close()


@connection.connection_handler
def get_question_id(cursor: RealDictCursor, id):
    query = """
        SELECT question_id
        FROM question_tag WHERE tag_id IN (%s);
        """
    cursor.execute(query, (id,))
    return cursor.fetchall()


@connection.connection_handler
def add_question_id_to_tag(cursor: RealDictCursor, question_id, tag_id):
    query = """
    INSERT INTO question_tag (question_id, tag_id)
    VALUES ((%s), (%s));
    """
    cursor.execute(query, (question_id, tag_id))
    cursor.close()


@connection.connection_handler
def get_new_user(cursor: RealDictCursor, new_user):
    query = """
        INSERT INTO users (username, registration_date,
        count_of_questions, count_of_answers, count_of_comments, reputation)
        VALUES (%(username)s, date_trunc('second', localtimestamp), 
        %(count_of_questions)s, %(count_of_answers)s, %(count_of_comments)s, %(reputation)s);
        """
    cursor.execute(query, new_user)
    cursor.close()


@connection.connection_handler
def get_all_tags(cursor: RealDictCursor):
    query = """
        SELECT name, count(name) AS usage
        FROM tag
        GROUP BY name;
        """
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def delete_tag_by_id(cursor: RealDictCursor, tag_id):
    query = """
        DELETE FROM question_tag WHERE tag_id IN (%s);
        DELETE FROM tag WHERE id IN (%s);
        """
    cursor.execute(query, (tag_id, tag_id))
    cursor.close()
