from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_user, login_required, logout_user,current_user
from .models import Note , Task, Journal
from Website import db
import json

views =Blueprint('views', __name__, template_folder= 'Templates')


@views.route('/about')
def about():
    return render_template('about.html', user = current_user)

@views.route('/profile')
def profile():
    return render_template('profile.html', user = current_user)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST': 
        note = request.form.get('note')#Gets the note from the HTML 
        title = request.form.get('title')
        
        if len(note) < 1:
            flash('Note is too short!', category='error') 
        else:
            new_note = Note(data=note,title=title ,user_id=current_user.id,)  #providing the schema for the note 
            db.session.add(new_note) #adding the note to the database 
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)





@views.route('/tasks',methods=['GET', 'POST'])
@login_required
def tasks():
    if request.method == 'POST': 
        task = request.form.get('task')#Gets the note from the HTML 
        title = request.form.get('title')
        
        if len(task) < 1:
            flash('Note is too short!', category='error') 
        else:
            new_task = Task(data = task ,title=title ,user_id=current_user.id)  #providing the schema for the note 
            db.session.add(new_task) #adding the task to the database 
            db.session.commit()
            flash('Task added!', category='success')

    return render_template('tasks.html', user = current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            flash('Note deleted', category='error')
            print('note deleted')
            db.session.delete(note)
            db.session.commit()
            
    return jsonify({})