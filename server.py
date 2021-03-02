from flask import Flask, redirect, render_template, request, session, escape
import data_manager
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['UPLOAD_IMAGE'] = "static/uploaded_images"
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route("/")
@app.route("/list")
def main():
    session_message = "You are not logged in"
    search = request.args.get('searched')
    sort = request.args.get('sort')
    if 'username' in session:
        session_message = 'Hello, %s' % escape(session['username'])
    if search:
        questions = data_manager.search_by_word(search)
    elif sort:
        sort = request.args.get('sort')
        order = request.args.get('order')
        if order == 'ascending':
            questions = data_manager.get_sorted_questions_asc(sort)
        else:
            questions = data_manager.get_sorted_questions_desc(sort)
    else:
        questions = data_manager.get_last_few_questions()
    return render_template("list.html", questions=questions, message=session_message)


@app.route("/question/<question_id>")
def question(question_id):
    question = data_manager.get_question(question_id)
    answers = data_manager.get_answers_by_question_id(question_id)
    comments = data_manager.get_all_comments()
    tag_ids = data_manager.get_tag_by_question_id(question_id)
    tags = []
    for id in tag_ids:
        tags.append(data_manager.get_tag_by_id(id['tag_id']))
    return render_template("question.html", question=question, question_id=question_id, answers=answers,
                           comments=comments, tags=tags)


@app.route("/question/<question_id>/new-answer")
def new_answer(question_id):
    return render_template("answer.html", question_id=question_id)


@app.route("/question/<question_id>/new-comment")
def new_question_comment(question_id):
    return render_template("comment.html", question_id=question_id, answer_id=None)


@app.route("/answer/<answer_id>/new-comment")
def new_answer_comment(answer_id):
    return render_template("comment.html", question_id=None, answer_id=answer_id)


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
        with open("fullpath.txt", "w") as path:
            path.write("<null>")
        return redirect("/list")
    else:
        return render_template("add-question.html")


@app.route("/question/<question_id>/edit", methods=['GET', 'POST'])
def edit_question(question_id):
    questions = data_manager.get_question(question_id)
    for question in questions:
        title = question['title']
        message = question['message']
    if request.method == 'POST':
        for question in questions:
            question['title'] = request.form['title']
            question['message'] = request.form['message']
            with open("fullpath.txt") as path:
                image = path.readline()
                if image != "<null>":
                    question['image'] = image
            data_manager.edit_question(question)
        return redirect(f"/question/{question_id}")
    else:
        return render_template("edit-question.html", title=title, message=message, question_id=question_id)


@app.route("/answer/<answer_id>/edit", methods=['GET', 'POST'])
def edit_answer(answer_id):
    answers = data_manager.get_answer_by_id(answer_id)
    for answer in answers:
        message = answer['message']
        question_id = answer['question_id']
    if request.method == 'POST':
        data_manager.delete_answer(answer_id)
        for answer in answers:
            answer['message'] = request.form['message']
            with open("fullpath.txt") as path:
                image = path.readline()
                if image != "<null>":
                    answer['image'] = image
        data_manager.write_answers(answer)
        return redirect(f"/question/{question_id}")
    else:
        return render_template("edit-answer.html", answer_id=answer_id, message=message, question_id=question_id)


@app.route("/comment/<comment_id>/edit", methods=['GET', 'POST'])
def edit_comment(comment_id):
    comments = data_manager.get_comment_by_id(comment_id)
    for comment in comments:
        message = comment['message']
        if comment['question_id']:
            question_id = comment['question_id']
        else:
            answers = data_manager.get_answer_by_id(comment['answer_id'])
            for a in answers:
                question_id = a['question_id']
    if request.method == 'POST':
        data_manager.delete_comment(comment_id)
        for comment in comments:
            comment['message'] = request.form['message']
        data_manager.write_comments(comment)
        return redirect(f"/question/{question_id}")
    else:
        return render_template("edit-comment.html", comment_id=comment_id, message=message, question_id=question_id)


@app.route("/answer", methods=['GET', 'POST'])
def answer():
    answer = {}
    if request.method == 'POST':
        question_id = request.form['question_id']
        last_answer = data_manager.get_last_answer()
        for a in last_answer:
            last_id = a['max']
        answer['message'] = request.form['answer']
        if last_id:
            answer['id'] = int(last_id) + 1
        else:
            answer['id'] = 1
        answer['submission_time'] = 0
        answer['vote_number'] = 0
        with open("fullpath.txt") as path:
            image = path.readline()
        answer['image'] = image
        answer['question_id'] = question_id
        data_manager.write_answers(answer)
        with open("fullpath.txt", "w") as path:
            path.write("<null>")
        return redirect(f"/question/{question_id}")
    else:
        return render_template("answer.html")


@app.route("/comment", methods=['GET', 'POST'])
def comment():
    comment = {}
    if request.method == 'POST':
        question_id = request.form['question_id']
        answer_id = request.form['answer_id']
        last_comment = data_manager.get_last_comment()
        for c in last_comment:
            last_id = c['max']
        comment['message'] = request.form['comment']
        if last_id:
            comment['id'] = int(last_id) + 1
        else:
            comment['id'] = 1
        comment['submission_time'] = 0
        comment['edited_count'] = 0
        if question_id != 'None':
            comment['question_id'] = question_id
            comment['answer_id'] = None
        else:
            comment['question_id'] = None
            comment['answer_id'] = answer_id
            answers = data_manager.get_answer_by_id(answer_id)
            for answer in answers:
                question_id = answer['question_id']
        data_manager.write_comments(comment)
        return redirect(f"/question/{question_id}")
    else:
        return render_template("comment.html")


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


@app.route("/comment/<comment_id>/delete", methods=['GET', 'POST'])
def delete_comment(comment_id):
    comment = data_manager.get_comment_by_id(comment_id)
    for c in comment:
        if c['question_id']:
            question_id = c['question_id']
        else:
            answers = data_manager.get_answer_by_id(c['answer_id'])
            for a in answers:
                question_id = a['question_id']
    data_manager.delete_comment(comment_id)
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


@app.route('/question/<question_id>/vote-up', methods=['GET', 'POST'])
def vote_up_question(question_id):
    if request.method == 'POST':
        questions = data_manager.get_question(question_id)
        for question in questions:
            question['vote_number'] += 1
            data_manager.edit_question(question)
        return redirect('/')


@app.route('/question/<question_id>/vote-down', methods=['GET', 'POST'])
def vote_down_question(question_id):
    if request.method == 'POST':
        questions = data_manager.get_question(question_id)
        for question in questions:
            question['vote_number'] -= 1
            data_manager.edit_question(question)
        return redirect('/')


@app.route('/question/<question_id>/upvote-answer/<answer_id>', methods=['GET', 'POST'])
def upvote_answer(question_id, answer_id):
    if request.method == 'POST':
        answers = data_manager.get_answers_by_question_id(question_id)
        for a in answers:
            if a['id'] == int(answer_id):
                data_manager.up_vote(answer_id)
        return redirect(f'/question/{question_id}')


@app.route('/question/<question_id>/downvote-answer/<answer_id>', methods=['GET', 'POST'])
def downvote_answer(question_id, answer_id):
    if request.method == 'POST':
        answers = data_manager.get_answers_by_question_id(question_id)
        for a in answers:
            if a['id'] == int(answer_id):
                data_manager.down_vote(answer_id)
        return redirect(f'/question/{question_id}')


@app.route('/question/<question_id>/new-tag', methods=['GET', 'POST'])
def new_tag(question_id):
    if request.method == 'POST':
        tags = {}
        tag = request.form['new-tag']
        last_tag = data_manager.get_last_tag()
        for t in last_tag:
            last_id = t['max']
        tags['id'] = int(last_id) + 1
        tags['name'] = tag
        data_manager.add_new_tag(tags)
        data_manager.add_question_id_to_tag(question_id, tags['id'])
        return redirect(f'/question/{question_id}')
    else:
        return render_template("add-tag.html", question_id=question_id, )


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    user = {}
    if request.method == 'POST':
        user['username'] = request.form['username']
        user['count_of_questions'] = 0
        user['count_of_answers'] = 0
        user['count_of_comments'] = 0
        user['reputation'] = 0
        data_manager.get_new_user(user)
        return redirect('/')
    return render_template('registration.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        # session['password'] = request.form['password']
        return redirect('/')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username')
    return redirect('/')

@app.route('/tags')
def tags():
    all_tag = data_manager.get_all_tags()
    return render_template("tags.html", all_tag=all_tag)


if __name__ == "__main__":
    app.run(
        debug=True
    )
