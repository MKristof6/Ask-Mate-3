import connection


def get_answers(question_id):
    answers = []
    data, header = connection.read_data("./sample_data/answer.csv")
    for answer in data:
        if answer["question_id"] == str(question_id):
            answers.append(answer)
    return answers, header


def get_all_answers():
    answers = []
    data, header = connection.read_data("./sample_data/answer.csv")
    for answer in data:
        answers.append(answer)
    return answers, header

def get_questions():
    questions, header = connection.read_data("./sample_data/question.csv")
    return questions, header

def write_answers(posts, header):
    connection.write_data("./sample_data/answer.csv", posts, header)

def write_question(posts, header):
    connection.write_data("./sample_data/question.csv", posts, header)