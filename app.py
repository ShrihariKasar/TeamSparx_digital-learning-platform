import os
import json
from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from config import Config

# ----------------------------
# Initialize App & Database
# ----------------------------
app = Flask(__name__, static_folder='static', template_folder='templates')
app.config.from_object(Config)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

os.makedirs(os.path.join(app.root_path, 'instance'), exist_ok=True)
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# ----------------------------
# Database Models
# ----------------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='student')  # student, teacher, admin

class Content(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(255), nullable=False)
    options = db.Column(db.Text)  # JSON string of options
    answer = db.Column(db.String(255), nullable=False)

    def get_options(self):
        try:
            return json.loads(self.options)
        except:
            return []

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(255))
    message = db.Column(db.Text)
    status = db.Column(db.String(20), default='Pending')
    created_by = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Initialize database
with app.app_context():
    db.create_all()

# ----------------------------
# Authentication Routes
# ----------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Check user in DB
        user = User.query.filter_by(username=email).first()

        if user and check_password_hash(user.password_hash, password):
            session['username'] = user.username
            session['role'] = user.role
            flash("Login successful!", "success")
            return redirect(url_for('dashboard'))
        else:
            error = "Invalid email or password"

    return render_template("login.html", error=error)
@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully', 'success')
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form.get('role', 'student')
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'danger')
            return redirect(url_for('register'))
        user = User(username=username, password_hash=generate_password_hash(password), role=role)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

# ----------------------------
# Index & Dashboard Routes
# ----------------------------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        flash('Please log in first.', 'warning')
        return redirect(url_for('login'))

    role = session.get('role')
    if role == 'student':
        return redirect(url_for('student_dashboard'))
    elif role == 'teacher':
        return redirect(url_for('teacher_dashboard'))
    elif role == 'admin':
        return redirect(url_for('admin_dashboard'))
    
    # fallback
    return render_template('index.html')

# ----------------------------
# CMS Routes
# ----------------------------
@app.route('/content', methods=['GET', 'POST'])
def list_content():
    if request.method == 'POST':
        if session.get('role') != 'teacher':
            flash('Access denied', 'danger')
            return redirect(url_for('list_content'))

        title = request.form.get('title', '').strip()
        file = request.files.get('file')

        if not title or not file:
            flash('Title and file are required.', 'danger')
            return redirect(url_for('list_content'))

        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        content = Content(title=title, filename=filename)
        db.session.add(content)
        db.session.commit()
        flash('Content uploaded successfully', 'success')
        return redirect(url_for('list_content'))

    # GET request
    contents = Content.query.order_by(Content.uploaded_at.desc()).all()
    return render_template('content.html', contents=contents)

# ----------------------------
# Quiz Routes
# ----------------------------

# List all quizzes
@app.route('/quizzes')
def list_quizzes():
    quizzes = Quiz.query.order_by(Quiz.id.desc()).all()
    return render_template('quiz_list.html', quizzes=quizzes)

# Take a quiz
@app.route('/quizzes/<int:quiz_id>', methods=['GET', 'POST'])
def take_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)

    if request.method == 'POST':
        score = 0
        total = len(quiz.questions)

        for question in quiz.questions:
            selected_option_id = request.form.get(f'question_{question.id}')
            if selected_option_id:
                selected_option = Option.query.get(int(selected_option_id))
                if selected_option and selected_option.is_correct:
                    score += 1

        feedback = {
            "score": score,
            "total": total,
            "message": "Perfect score! Well done!" if score == total else "Keep practicing!"
        }
        return render_template('take_quiz.html', quiz=quiz, feedback=feedback)

    return render_template('take_quiz.html', quiz=quiz)

# ----------------------------
# Teacher: Create new quiz
# ----------------------------
@app.route('/teacher/quiz/new', methods=['GET', 'POST'])
def new_quiz():
    if 'username' not in session or session.get('role') != 'teacher':
        flash("Access denied", "danger")
        return redirect(url_for('list_quizzes'))

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()

        if not title:
            flash("Quiz title is required.", "danger")
            return render_template('teacher_new_quiz.html')

        quiz = Quiz(title=title, description=description)
        db.session.add(quiz)
        db.session.commit()
        flash("Quiz created successfully! You can now add questions.", "success")
        return redirect(url_for('add_questions', quiz_id=quiz.id))

    return render_template('teacher_new_quiz.html')

# ----------------------------
# Teacher Dashboard
# ----------------------------
@app.route('/teacher')
def teacher_dashboard():
    if session.get('role') != 'teacher':
        flash('Access denied', 'danger')
        return redirect(url_for('dashboard'))
    stats = {
        'classes_count': 5,
        'students_count': 30,
        'pending_quizzes': 3,
        'avg_progress': '75%'
    }
    return render_template('teacher_dashboard.html', stats=stats)

# ----------------------------
# Student Dashboard
# ----------------------------
@app.route('/student')
def student_dashboard():
    if session.get('role') != 'student':
        flash('Access denied', 'danger')
        return redirect(url_for('dashboard'))
    stats = {
        'lessons_completed': 12,
        'pending_quizzes': 2,
        'completed_quizzes': 5,
        'progress': '60%'
    }
    return render_template('student_dashboard.html', stats=stats)

# ----------------------------
# Community Routes
# ----------------------------
@app.route('/community')
def community_forum():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('community.html', posts=posts)

@app.route('/community/new', methods=['POST'])
def new_post():
    title = request.form['title']
    content = request.form['content']
    author = session.get('username', 'Anonymous')
    post = Post(title=title, content=content, author=author)
    db.session.add(post)
    db.session.commit()
    flash('Post created successfully', 'success')
    return redirect(url_for('community_forum'))

# ----------------------------
# Support Routes
# ----------------------------
@app.route('/support')
def support_home():
    if 'username' not in session:
        flash('Please log in first.', 'warning')
        return redirect(url_for('login'))

    tickets = Ticket.query.filter_by(created_by=session.get('username')) \
                          .order_by(Ticket.created_at.desc()).all()
    return render_template('support.html', tickets=tickets)


# Submit new ticket
@app.route('/support/new', methods=['GET', 'POST'])
def submit_ticket():
    if 'username' not in session:
        flash('Please log in first.', 'warning')
        return redirect(url_for('login'))

    if request.method == 'POST':
        subject = request.form.get('subject', '').strip()
        message = request.form.get('message', '').strip()

        if not subject or not message:
            flash('Subject and message are required.', 'danger')
            return render_template('submit_ticket.html')

        ticket = Ticket(
            subject=subject,
            message=message,
            created_by=session.get('username')
        )
        db.session.add(ticket)
        db.session.commit()
        flash('Ticket submitted successfully!', 'success')
        return redirect(url_for('support_home'))

    return render_template('submit_ticket.html')


# View a single ticket
@app.route('/support/ticket/<int:ticket_id>')
def view_ticket(ticket_id):
    if 'username' not in session:
        flash('Please log in first.', 'warning')
        return redirect(url_for('login'))

    ticket = Ticket.query.get_or_404(ticket_id)

    # Only allow ticket owner or admin to view
    if ticket.created_by != session.get('username') and session.get('role') != 'admin':
        flash('Access denied.', 'danger')
        return redirect(url_for('support_home'))

    return render_template('view_ticket.html', ticket=ticket)
# ----------------------------
# Monitor / Analytics Route
# ----------------------------
@app.route('/monitor')
def monitor():
    if session.get('role') not in ['teacher', 'admin']:
        flash('Access denied', 'danger')
        return redirect(url_for('dashboard'))

    stats = {
        'users_count': User.query.count(),
        'lessons_count': Content.query.count(),
        'quizzes_count': Quiz.query.count(),
        'tickets_count': Ticket.query.count(),
        'weeks': ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
        'progress_data': [10, 25, 40, 60],
        'quiz_labels': ['Quiz 1', 'Quiz 2', 'Quiz 3', 'Quiz 4'],
        'quiz_scores': [80, 85, 90, 75],
        'class_labels': ['Active', 'Inactive'],
        'class_data': [70, 30]
    }
    return render_template('monitor.html', stats=stats)

# ----------------------------
# Admin Routes
# ----------------------------
@app.route('/admin')
def admin_dashboard():
    if session.get('role') != 'admin':
        flash('Access denied', 'danger')
        return redirect(url_for('dashboard'))
    stats = {
        'total_students': User.query.filter_by(role='student').count(),
        'total_teachers': User.query.filter_by(role='teacher').count(),
        'total_lessons': Content.query.count(),
        'total_quizzes': Quiz.query.count()
    }
    return render_template('admin.html', stats=stats)

# ----------------------------
# Run App
# ----------------------------
if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.run(debug=True)