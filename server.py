from flask import Flask, redirect, render_template, request
import data_manager
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['UPLOAD_IMAGE'] = "static/uploaded_images"


@app.route("/")
@app.route("/list")
def list():
    questions = data_manager.get_questions()
    return render_template("list.html", questions=questions)


@app.route("/question/<question_id>")
def question(question_id):
    question = data_manager.get_question(question_id)
    answers= data_manager.get_answers(question_id)
    return render_template("question.html", question=question, question_id = question_id, answers=answers)


@app.route("/question/<question_id>/new-answer")
def new_answer(question_id):
    return render_template("answer.html", question_id=question_id)


@app.route("/add-question", methods=['GET', 'POST'])
def add_question():
    last_question = data_manager.get_last_question()
    for q in last_question:
        last_id = q['max']
    question = {}
    if request.method == 'POST':
        question['title'] = request.form['title']
        question['message'] = request.form['message']
        question['id'] = int(last_id) + 1
        question['submission_time'] = 0
        question['view_number'] = 0
        question['vote_number'] = 0
        with open("fullpath.txt") as path:
            image = path.readline()
        question['image'] = image
        data_manager.write_question(question)
        return redirect("/list")
    else:
        return render_template("add-question.html")


@app.route("/question/<question_id>/edit", methods=['GET', 'POST'])
def edit_question(question_id):
    questions = data_manager.get_questions()
    if request.method == 'POST':
        for question in questions:
            if question['id'] == question_id:
                question['title'] = request.form['title']
                question['message'] = request.form['message']
        data_manager.write_question(question)
        return redirect(f"/question/{question_id}")
    else:
        for question in questions:
            if question['id'] == question_id:
                title = question['title']
                message = question['message']
        return render_template("edit-question.html", title=title, message=message, question_id=question_id)


# @app.route("/answer/<answer-id>/edit", methods=['GET', 'POST'])
# def edit_answer(answer_id):

@app.route("/answer", methods=['GET', 'POST'])
def answer():
    answer = {}
    if request.method == 'POST':
        question_id = request.form['question_id']
        last_answer = data_manager.get_last_answer(question_id)
        for a in last_answer:
            last_id = a['max']
        answer['message'] = request.form['answer']
        if last_id:
            answer['id'] = int(last_id) + 1
        else:
            answer['id'] = 1
        answer['submission_time'] = 0
        answer['vote_number'] = 0
        answer['image'] = 'image placeholder'
        answer['question_id'] = question_id
        data_manager.write_answers(answer)
        return redirect(f"/question/{question_id}")
    else:
        return render_template("answer.html")


@app.route("/question/<question_id>/delete")
def delete_question(question_id):
    data_manager.delete_question(question_id)
    return redirect("/")


@app.route("/answer/<answer_id>/delete", methods=['GET', 'POST'])
def delete_answer(answer_id):
    answer = data_manager.get_answer_by_id(answer_id)
    for a in answer:
        question_id = a['question_id']
    data_manager.delete_answer(answer_id)
    return redirect(f"/question/{question_id}")


@app.route('/selector', methods=['GET', 'POST'])
def selector():
    if request.method == 'POST':
        f = request.files['file']
        f.save(os.path.join(app.config['UPLOAD_IMAGE'], secure_filename(f.filename)))
        fullpath = f.filename
        with open("fullpath.txt", "w") as path:
            path.write(fullpath)
        return "image successfully uploaded"
    else:
        return render_template("selector.html")


# @app.route('/question/<question_id>/vote-up')
# def vote_up_questions(question_id):
#     questions, header = data_manager.get_questions()
#     for question in questions:
#         if question['id'] == question_id:
#
#             question['title'] = question['title']
#             question['message'] = question['message']
#             question['id'] = question_id
#             question['submission_time'] = question['submission_time']
#             question['vote_number'] = int(question['vote_number']) + 1
#             question['image'] = question['image']
#             questions.append(question)
#             data_manager.write_question(questions, header)
#             return redirect("/question/{{ question_id }}")


# @app.route("/get-image/<image_name>")
# def get_image(image_name):
#
#     try:
#         return send_from_directory(app.config["CLIENT_IMAGES"], filename=image_name, as_attachment=True)
#     except FileNotFoundError:
#         abort(404)


if __name__ == "__main__":
    app.run(
        debug=True
    )
