from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from .models import Note, Task, User, Business
from Website import db
import json

views = Blueprint('views', __name__, template_folder='Templates')


@views.route('/about')
def about():
    return render_template('about.html', user=current_user)


@views.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        biz_name = request.form.get('biz_name')
        biz_desc = request.form.get('title')

        # If you plan to save a business entry, uncomment and adjust below:
        # if biz_name and biz_desc:
        #     new_business = Business(name=biz_name, description=biz_desc, user_id=current_user.id)
        #     db.session.add(new_business)
        #     db.session.commit()
        #     flash('Business info saved!', category='success')

    return render_template('profile.html', user=current_user)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')
        title = request.form.get('title')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, title=title, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/tasks', methods=['GET', 'POST'])
@login_required
def tasks():
    if request.method == 'POST':
        task = request.form.get('task')
        title = request.form.get('title')

        if len(task) < 1:
            flash('Task is too short!', category='error')
        else:
            new_task = Task(data=task, title=title, user_id=current_user.id)
            db.session.add(new_task)
            db.session.commit()
            flash('Task added!', category='success')

    return render_template('tasks.html', user=current_user)


@views.route('/delete-note', methods=['POST'])
@login_required
def delete_note():
    note = json.loads(request.data)  # expects JSON from frontend
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note and note.user_id == current_user.id:
        db.session.delete(note)
        db.session.commit()
        flash('Note deleted', category='success')

    return jsonify({})
