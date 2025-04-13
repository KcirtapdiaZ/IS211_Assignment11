import os
import pickle
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

SAVE_FILE = 'todo_list.pkl'

if os.path.exists(SAVE_FILE):
    with open(SAVE_FILE, 'rb') as f:
        todo_items = pickle.load(f)
else:
    todo_items = []

@app.route('/')
def index():
    return render_template('index.html', items=todo_items)

@app.route('/submit', methods=['POST'])
def submit():
    task = request.form.get('task')
    email = request.form.get('email')
    priority = request.form.get('priority')

    if not task or not email or priority not in ['Low', 'Medium', 'High']:
        return redirect(url_for('index'))

    todo_items.append({'task': task, 'email': email, 'priority': priority})
    return redirect(url_for('index'))

@app.route('/clear', methods=['POST'])
def clear():
    global todo_items
    todo_items = []
    return redirect(url_for('index'))

@app.route('/save', methods=['POST'])
def save():
    with open(SAVE_FILE, 'wb') as f:
        pickle.dump(todo_items, f)
    return redirect(url_for('index'))

@app.route('/delete/<int:item_id>', methods=['POST'])
def delete(item_id):
    if 0 <= item_id < len(todo_items):
        todo_items.pop(item_id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
