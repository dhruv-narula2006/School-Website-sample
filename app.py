from flask import Flask, render_template, redirect, request, flash, url_for
from flask_login import LoginManager, login_user, login_required,logout_user, current_user
import os
from extensions import db
from models import Parent, Student, Document
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'secret123'
app.config['UPLOAD_FOLDER'] = 'uploads'

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return Parent.query.get(int(user_id))


# ---------------- ROUTES ---------------- #

@app.route('/')
def home():
    return render_template("index.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = generate_password_hash(request.form.get('password'))

        user = Parent(name=name, email=email, password=password)
        db.session.add(user)
        db.session.commit()

        flash("Registered Successfully")
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = Parent.query.filter_by(email=request.form.get('email')).first()

        if user and check_password_hash(user.password, request.form.get('password')):
            login_user(user)
            return redirect(url_for('dashboard'))

        flash("Invalid Credentials")

    return render_template('login.html')


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


@app.route('/upload', methods=['POST'])
@login_required
def upload():
    file = request.files['file']

    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        doc = Document(filename=file.filename)
        db.session.add(doc)
        db.session.commit()

        flash("File Uploaded!")

    return redirect(url_for('dashboard'))


@app.route('/events')
def events():
    return [
        {"title": "Sports Day", "start": "2026-04-10", "grade": "10"},
        {"title": "Exam Week", "start": "2026-04-15", "grade": "12"},
        {"title": "Science Fair", "start": "2026-04-20", "grade": "9"}
    ]

@app.route('/admin')
@login_required
def admin():
    if not current_user.is_admin:
        return "Access Denied"
    students = Student.query.all()
    return render_template('admin.html', students=students)

@app.route('/admission', methods=['GET', 'POST'])
@login_required
def admission():
    if request.method == 'POST':
        student = Student(
            name=request.form['name'],
            grade=request.form['grade'],
            dob=request.form['dob'],
            address=request.form['address'],
            parent_id=current_user.id
        )
        db.session.add(student)
        db.session.commit()

        flash("Admission submitted!")
        return redirect('/dashboard')

    return render_template('admission.html')


@app.route('/calendar')
def calendar():
    return render_template('/calendar.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')

@app.route('/contact',methods=['POST'])
def contact():
    flash("Message sent successfully!")
    return redirect('/')

# ---------------- RUN ---------------- #

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)