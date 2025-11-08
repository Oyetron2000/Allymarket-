from flask import Blueprint, current_app, redirect, render_template, request, flash, jsonify, url_for
from flask_login import login_user, login_required, logout_user, current_user
from .models import Note, Task, User, Business
from Website import db
from werkzeug.utils import secure_filename
import os
import json

views = Blueprint('views', __name__, template_folder='Templates')


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@views.route('/about')
def about():
    return render_template('about.html', user=current_user)


@views.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    VALID_CATEGORIES = [
        "Food & Beverage",
        "Retail",
        "Services",
        "Health & Wellness",
        "Arts & Crafts",
    ]

    if request.method == 'POST':
        # --- PROFILE PICTURE UPLOAD ---
        file = request.files.get('profile_image')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            upload_folder = os.path.join(current_app.root_path, 'static/uploads/profiles')
            os.makedirs(upload_folder, exist_ok=True)
            file.save(os.path.join(upload_folder, filename))

            current_user.profile_image = filename
            db.session.commit()
            flash("Profile picture updated successfully!", "success")
            return redirect(url_for('views.profile'))

        # --- BUSINESS CREATION (with optional image) ---
        biz_name = (request.form.get('biz_name') or '').strip()
        biz_desc = (request.form.get('biz_desc') or '').strip()
        biz_cat  = (request.form.get('biz_cat') or '').strip()
        biz_image = request.files.get('biz_image')

        errors = []
        if not biz_name:
            errors.append("Please enter a business name.")
        if biz_cat not in VALID_CATEGORIES:
            errors.append("Please select a valid category.")

        if errors:
            for e in errors:
                flash(e, category='error')
        else:
            biz_filename = None
            if biz_image and allowed_file(biz_image.filename):
                biz_filename = secure_filename(biz_image.filename)
                biz_folder = os.path.join(current_app.root_path, 'static/uploads/businesses')
                os.makedirs(biz_folder, exist_ok=True)
                biz_image.save(os.path.join(biz_folder, biz_filename))

            new_business = Business(
                biz_name=biz_name,
                description=biz_desc,
                category=biz_cat,
                image_file=biz_filename,
                user_id=current_user.id
            )
            db.session.add(new_business)
            current_user.biz_added = True
            db.session.commit()
            flash('Business added successfully!', category='success')
            return redirect(url_for('views.profile'))

    # --- GET REQUEST (or failed POST) ---
    businesses = Business.query.filter_by(user_id=current_user.id) \
                               .order_by(Business.created_at.desc()) \
                               .all()
    return render_template('profile.html', user=current_user, businesses=businesses)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    businesses = Business.query.order_by(Business.created_at.desc()).all()
    return render_template('home.html', user=current_user, businesses=businesses)

@views.route('/tasks', methods=['GET', 'POST'])
@login_required
def tasks():
    search_query = request.args.get('q', '').strip()

    if search_query:
        # Filter by name, description, or category (case-insensitive)
        businesses = Business.query.filter(
            (Business.biz_name.ilike(f"%{search_query}%")) |
            (Business.description.ilike(f"%{search_query}%")) |
            (Business.category.ilike(f"%{search_query}%"))
        ).order_by(Business.created_at.desc()).all()
    else:
        businesses = Business.query.order_by(Business.created_at.desc()).all()

    return render_template('discover.html', user=current_user, businesses=businesses, search_query=search_query)


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

