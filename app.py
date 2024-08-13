from flask import Flask, render_template, request, redirect, url_for
import datetime

app = Flask(__name__)
todos = [{'todo': 'Sample Todo', 'done': False}]

@app.route('/')
def index():
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    return render_template('index.html', todos=todos, current_time=current_time)

@app.route('/add', methods=['POST'])
def add_todo():
    todo = request.form['todo']
    todos.append({'todo': todo, 'done': False})
    return redirect(url_for('index'))

@app.route('/mark_done/<int:index>', methods=['POST'])
def mark_done(index):
    if request.method == 'POST':
        todos[index]['done'] = True
        return redirect(url_for('index'))

@app.route('/delete/<int:index>', methods=['POST'])
def delete(index):
    if request.method == 'POST':
        del todos[index]
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
