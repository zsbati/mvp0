# app.py
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from forms import RegistrationForm, ChangePasswordForm
from models import db, User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/create_superuser')
def create_superuser():
    if User.query.filter_by(username='admin').first() is None:  # Check if superuser exists
        superuser = User(username='admin', password='admin_password', role='superuser')
        db.session.add(superuser)
        db.session.commit()
        return "Superuser created!"
    return "Superuser already exists!"


@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.password == form.old_password.data:
            current_user.password = form.new_password.data
            db.session.commit()
            flash('Password changed successfully!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Old password is incorrect.', 'danger')
    return render_template('change_password.html', form=form)


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    if current_user.role != 'superuser':
        flash('You do not have permission to edit users.', 'danger')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        new_role = request.form.get('role')
        user.role = new_role
        db.session.commit()
        flash('User role updated successfully!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('edit_user.html', user=user)


@app.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if current_user.role != 'superuser':
        flash('You do not have permission to delete users.', 'danger')
        return redirect(url_for('dashboard'))

    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully!', 'success')
    return redirect(url_for('dashboard'))


@app.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    # Only allow superuser to register new accounts
    if current_user.role != 'superuser':
        flash('You do not have permission to register new accounts.', 'danger')
        return redirect(url_for('dashboard'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, password=form.password.data, role=form.role.data)
        db.session.add(user)
        db.session.commit()
        flash('Account created!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('register.html', form=form)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables
    app.run(debug=True)
