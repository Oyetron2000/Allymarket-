from flask import Blueprint, current_app, redirect, render_template, request, flash, jsonify, url_for
from flask_login import login_user, login_required, logout_user, current_user
from .models import Note, Review, Task, User, Business, Review
from Website import db
from werkzeug.utils import secure_filename
import os
import json

views = Blueprint('views', __name__, template_folder='Templates')


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_business_image(file):
    """
    Saves an uploaded business image to the static/uploads/business folder.
    Returns the filename to store in the database.
    """
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        upload_folder = os.path.join(current_app.root_path, 'static/uploads/business')
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
        return filename
    return None

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
        biz_phone = (request.form.get('biz_phone') or '').strip()
        biz_email = (request.form.get('biz_email') or '').strip()
        location = (request.form.get('location') or '').strip()
        biz_site = (request.form.get('biz_site') or '').strip()
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
def home():
    businesses = Business.query.order_by(Business.created_at.desc()).all()
    return render_template('home.html', user=current_user, businesses=businesses)




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



@views.route("/business/<int:biz_id>/review", methods=["POST"])
@login_required
def add_review(biz_id):
    business = Business.query.get_or_404(biz_id)

    # 🚫 Business owners cannot review their own business
    if current_user.id == business.user_id:
        flash("You cannot review your own business.", "danger")
        return redirect(url_for("views.business_page", biz_id=biz_id))

    rating = int(request.form.get("rating"))
    content = request.form.get("content")

    if rating < 1 or rating > 5:
        flash("Invalid rating.", "danger")
        return redirect(url_for("views.business_page", biz_id=biz_id))

    review = Review(
        rating=rating,
        content=content,
        user_id=current_user.id,
        business_id=biz_id
    )

    db.session.add(review)
    db.session.commit()

    flash("Review submitted!", "success")
    return redirect(url_for("views.business_page", biz_id=biz_id))

    flash("Review submitted!", "success")
    return redirect(url_for('views.business_page', biz_id=biz_id))

#gets the business id for the business page
@views.route('/business/<int:biz_id>')
def business_page(biz_id):
    business = Business.query.get_or_404(biz_id)
    reviews = Review.query.filter_by(business_id=biz_id).order_by(Review.created_at.desc()).all()

    return render_template("business_page.html", business=business, user=current_user, reviews=reviews)

