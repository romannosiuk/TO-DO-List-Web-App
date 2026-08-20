import os
from datetime import datetime, timezone
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_login import login_user, logout_user, current_user, UserMixin, LoginManager, login_required
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Boolean, DateTime, ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash
from forms import RegisterForm, LoginForm

# Flask App
app = Flask(__name__,
            template_folder='app/templates',
            static_folder='app/static',
            static_url_path='/static')

# Config
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "instance", "data.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'

# Flask-Bootstrap
bootstrap = Bootstrap(app)
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
db.init_app(app)

# Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Models
class User(UserMixin, db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    tasks: Mapped[list['Task']] = relationship('Task', back_populates='user', cascade='all, delete-orphan')


class Task(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(String(1000), nullable=True)
    completed: Mapped[bool] = mapped_column(Boolean, default=False)
    priority: Mapped[int] = mapped_column(Integer, default=1)
    due_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    user: Mapped['User'] = relationship('User', back_populates='tasks')

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# Demo user setup
def create_demo_user():
    with app.app_context():
        existing_user = db.session.execute(
            db.select(User).where(User.username == 'test')
        ).scalar_one_or_none()

        if not existing_user:
            demo_user = User(
                username='test',
                email='test@gmail.com',
                password_hash='0123450'
            )
            db.session.add(demo_user)
            db.session.commit()
            print("Demo user created: test / test@gmail.com")
        else:
            print("Demo user already exists")

def get_all_tasks():
    tasks = current_user.tasks
    sorted_tasks = sorted(tasks, key=lambda task: (task.completed, -task.priority))
    return render_template('index.html', tasks=sorted_tasks)

# Create tables and demo user
with app.app_context():
    db.create_all()
    create_demo_user()

# Routes
@app.route('/')
@login_required
def index():
    return get_all_tasks()

@app.route('/tasks', methods=['POST'])
@login_required
def create_task():
    title = request.form.get('title')

    if not title:
        return redirect(url_for('index'))

    task = Task(title=title, user_id=current_user.id, priority=0)
    db.session.add(task)
    db.session.commit()

    return redirect(url_for('index'))

@app.route("/delete_task/<task_id>", methods=['POST'])
@login_required
def delete_task(task_id):
    task = db.session.execute(
        db.select(Task).where(Task.id == task_id)
    ).scalar_one_or_none()
    if task:
        db.session.delete(task)
        db.session.commit()
    return redirect(url_for('index'))

@app.route("/toggle_task/<task_id>", methods=['POST'])
@login_required
def toggle_task(task_id):
    task = db.session.execute(
        db.select(Task).where(Task.id == task_id)
    ).scalar_one_or_none()
    if task:
        task.completed = not task.completed
        db.session.commit()
    return redirect(url_for('index'))

@app.route("/edit_task/<task_id>", methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    task = db.session.execute(
        db.select(Task).where(Task.id == task_id)
    ).scalar_one_or_none()

    if not task:
        return redirect(url_for('index'))

    return render_template('edit_task.html', task=task)

@app.route("/update_task/<task_id>", methods=['POST'])
@login_required
def update_task(task_id):
    task = db.session.execute(
        db.select(Task).where(Task.id == task_id)
    ).scalar_one_or_none()

    if task:
        task.title = request.form.get('title')
        db.session.commit()

    return redirect(url_for('index'))

@app.route("/priority_task/<task_id>", methods=['POST'])
@login_required
def priority_task(task_id):
    task = db.session.execute(
        db.select(Task).where(Task.id == task_id)
    ).scalar_one_or_none()
    if task:
        task.priority = 1 if task.priority == 0 else 0
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        result = db.session.execute(db.select(User).where(User.email == form.email.data))
        user = result.scalar()
        if user:
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('login'))
        
        hash_and_salted_password = generate_password_hash(
            form.password.data,
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = User(
            email=form.email.data,
            username=form.name.data,
            password_hash=hash_and_salted_password,
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("index"))
    return render_template("register.html", form=form, current_user=current_user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        result = db.session.execute(db.select(User).where(User.email == email))
        user = result.scalar()

        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('index'))

    return render_template("login.html", form=form)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run()
