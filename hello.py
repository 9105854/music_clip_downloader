from flask import Flask, make_response, render_template, request, url_for
from automatic_clip_downloader import download_songs
from werkzeug.utils import secure_filename
import uuid
import sqlite3
import threading
app = Flask(__name__)
connection = sqlite3.connect("jobs.db")
cursor = connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS jobs (job_id STRING NOT NULL PRIMARY KEY,  progress INTEGER, final_file STRING)")
connection.commit()
@app.route('/')
def hello_world():
    return render_template("index.html")

@app.route('/job/progress', methods=['GET'])
def job_progress(): 
    # get progress 
    db_connection = sqlite3.connect('jobs.db')
    cursor = db_connection.cursor()
    job_id = request.headers.get("Job-ID")
    print(job_id)
    progress = cursor.execute(f"SELECT progress FROM jobs WHERE job_id = '{job_id}'").fetchone()[0]
    print(progress)
        
    response = make_response(render_template('progress_bar.html', progress_percent=progress))

    if progress == 100:
        response.headers.set("HX-Trigger", 'done')
    return response
@app.route('/job', methods=["GET"])
def job():
    db_connection = sqlite3.connect('jobs.db')
    cursor = db_connection.cursor()
    job_id = request.headers.get("Job-ID")
    final_file = cursor.execute(f"SELECT final_file FROM jobs WHERE job_id = '{job_id}'").fetchone()[0]
    url = url_for('static', filename=final_file)
    return f"<a href={url} download hx-boost='false'>Download zip here</a>"
@app.route('/upload', methods=['POST'])
def upload_file():
    finished_file = ''
        
    job_id = uuid.uuid4()
    f = request.files['file']
    file_name = secure_filename(f.filename)
    file_path = './song_lists/' + secure_filename(f.filename) 
    f.save(file_path)
    thread = threading.Thread(target=download_songs, args=(file_path, file_name, str(job_id)), daemon=True)
    thread.start()
    return render_template("upload_response.html", job_id=job_id)