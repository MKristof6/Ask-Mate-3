from flask import Flask, redirect, render_template
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
    answers = data_manager.get_answers(question_id)
    return render_template("question.html", question_id=question_id, question=question, answers = answers)

@app.route("/question/<question_id>/new-answer")
def new_answer(question_id):
    return render_template("answer.html", question_id=question_id)


@app.route("/add_question")
def add_question():
    return  render_template("add_question.html")

@app.route("/answer")
def answer():
    return redirect("/question")




if __name__ == "__main__":
    app.run(
        debug= True
    )
