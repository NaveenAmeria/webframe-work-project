from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import date, datetime
from models import db, Task

app = Flask(__name__)
app.secret_key = 'student_task_manager_secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()


# ── Routes ────────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    tasks = (
        Task.query
        .order_by(Task.completed.asc(), Task.deadline.asc())
        .all()
    )
    return render_template('index.html', tasks=tasks, today=date.today())


@app.route('/add', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        title       = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        deadline    = request.form.get('deadline', '').strip()

        if not title:
            flash('Task title is required.', 'danger')
            return redirect(url_for('add_task'))

        task = Task(
            title       = title,
            description = description or None,
            deadline    = datetime.strptime(deadline, '%Y-%m-%d').date() if deadline else None,
        )
        db.session.add(task)
        db.session.commit()

        flash(f'Task "{title}" added successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('add_task.html')


@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    task = Task.query.get_or_404(task_id)
    task.completed = not task.completed
    db.session.commit()

    label = 'marked as completed' if task.completed else 'marked as pending'
    flash(f'Task "{task.title}" {label}.', 'info')
    return redirect(url_for('index'))


@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()

    flash(f'Task "{task.title}" deleted.', 'warning')
    return redirect(url_for('index'))


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == '__main__':
    app.run(debug=True)
