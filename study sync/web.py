from flask import Flask, render_template, request, redirect, url_for, jsonify
import database
import os
app = Flask(__name__)
database.init_db()
@app.route('/', methods=['GET'])
def index():
    tasks = database.get_all_tasks()
    return render_template('index.html', tasks=tasks)
@app.route('/add', methods=['POST'])
def add_task():
    subject = request.form.get('subject', '').strip()
    task = request.form.get('task', '').strip()
    deadline = request.form.get('deadline', '').strip()
    priority = request.form.get('priority', 'Medium')
    duration_text = request.form.get('duration', '25').strip()
    if not subject or not task:
        return redirect(url_for('index'))
    try:
        duration = int(duration_text)
        if duration <= 0:
            duration = 25
    except ValueError:
        duration = 25
    database.add_task_to_db(subject, task, deadline, priority, duration)
    return redirect(url_for('index'))
@app.route('/complete/<int:task_id>', methods=['POST'])
def complete_task(task_id):
    database.complete_task_in_db(task_id)
    return jsonify(success=True)
if __name__ == '__main__':
    import webbrowser
    import threading
    import subprocess
    def open_browser():
        port = int(os.environ.get("PORT", 5000))
        url = f'http://0.0.0.0:{port}'
        try:
            webbrowser.open(url, new=2)
        except Exception:
            subprocess.Popen(['start', url], shell=True)
    if not os.environ.get("PORT"):
        timer = threading.Timer(2, open_browser)
        timer.daemon = True
        timer.start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)
