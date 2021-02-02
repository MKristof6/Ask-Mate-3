import connection


def get_answers(question_id):
    answers = []
    data, header = connection.read_data("./sample_data/answer.csv")
    for answer in data:
        if answer["question_id"] == str(question_id):
            answers.append(answer)
    return answers

def get_questions():
    questions, header = connection.read_data("./sample_data/question.csv")
    print(questions)
    return questions, header
