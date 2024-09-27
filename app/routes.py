from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db
from app.models import User, StudentProgress, TeacherComment
from app.forms import LoginForm, AddUserForm  # Import the new form


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:  # Use hashed passwords in production
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', form=form)


@app.route('/add_user', methods=['GET', 'POST'])
@login_required
def add_user():
    if current_user.role != 'admin':
        return redirect(url_for('dashboard'))  # Only allow admin to access this route

    form = AddUserForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, password=form.password.data, role=form.role.data)
        db.session.add(new_user)
        db.session.commit()
        flash('User added successfully!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('add_user.html', form=form)


@app.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if current_user.role != 'admin':
        return redirect(url_for('dashboard'))  # Only allow admin to access this route

    user_to_delete = User.query.get(user_id)
    if user_to_delete:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash('User deleted successfully!', 'success')
    return redirect(url_for('dashboard'))


@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    if current_user.role != 'admin':
        return redirect(url_for('dashboard'))  # Only allow admin to access this route

    form = ChangePasswordForm()
    if form.validate_on_submit():
        user_to_change = User.query.filter_by(username=form.username.data).first()
        if user_to_change:
            user_to_change.password = form.new_password.data  # Consider hashing the password
            db.session.commit()
            flash('Password changed successfully!', 'success')
        else:
            flash('User not found!', 'danger')
        return redirect(url_for('dashboard'))
    return render_template('change_password.html', form=form)

# Add other existing routes here...
