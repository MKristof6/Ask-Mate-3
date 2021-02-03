from flask import Flask, redirect, render_template, request
import data_manager

app = Flask(__name__)


@app.route("/")
@app.route("/list")
def list():
    questions, header = data_manager.get_questions()
    return render_template("list.html", questions=questions, header=header)


@app.route("/question/<question_id>")
def question(question_id):
    questions, header = data_manager.get_questions()
    question = {}
    for q in questions:
        if q['id'] == question_id:
            question = q
    answers, header = data_manager.get_answers(question_id)
    return render_template("question.html", question_id=question_id, question=question, answers=answers)


@app.route("/question/<question_id>/new-answer")
def new_answer(question_id):
    return render_template("answer.html", question_id=question_id)


@app.route("/add-question", methods=['GET', 'POST'])
def add_question():
    question = {}
    if request.method == 'POST':
        questions, header = data_manager.get_questions()
        question['title'] = request.form['title']
        question['message'] = request.form['question']
        question['id'] = int(questions[-1]['id']) + 1
        question['submission_time'] = 0
        question['view_number'] = 0
        question['vote_number'] = 0
        question['image'] = 'image placeholder'
        questions.append(question)
        data_manager.write_question(questions, header)
        return redirect("/list")
    else:
        return render_template("add-question.html")


@app.route("/answer", methods=['GET', 'POST'])
def answer():
    answer = {}
    if request.method == 'POST':
        question_id = request.form['question_id']
        answers, header = data_manager.get_answers(question_id)
        answer['message'] = request.form['answer']
        try:
            answer['id'] = int(answers[-1]['id']) + 1
        except IndexError:
            answer['id'] = 1
        answer['submission_time'] = 0
        answer['vote_number'] = 0
        answer['image'] = 'image placeholder'
        answer['question_id'] = question_id
        answers.append(answer)
        data_manager.write_answers(answers, header)
        return redirect(f"/question/{question_id}")
    else:
        return render_template("answer.html")


@app.route("/question/<question_id>/delete")
def delete_question(question_id):
    questions, header = data_manager.get_questions()
    for question in questions:
        if question['id'] == question_id:
            questions.remove(question)
            data_manager.write_question(questions, header)
    return redirect("/")

@app.route("/answer/<answer_id>/delete", methods= ['GET', 'POST'])
def delete_asnwer(answer_id):
    question_id = request.form["question_id"]
    answers, header = data_manager.get_answers(question_id)
    for answer in answers:
        if answer['id'] == answer_id:
            answers.remove(answer)
            data_manager.write_answers(answer, header)
    return redirect("/question/<question_id>")


if __name__ == "__main__":
    app.run(
        debug=True
    )
