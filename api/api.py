import json
from werkzeug.utils import secure_filename
from os import uname, path
from flask_cors import CORS
from flask_socketio import SocketIO
from flask import Flask, request, jsonify, make_response
from api_helper import format_file

rpi = uname()[4] != 'x86_64'

UPLOAD_FOLDER = 'cvs_files'
if rpi:
    UPLOAD_FOLDER = '/home/pi/pile-placer/api/cvs_files'

ALLOWED_EXTENSIONS = {'csv', 'xlsx'}

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'secret'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
socketio = SocketIO(app, cors_allowed_origins="*")

port = 10000


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return "... qc server running on port %s" % port


@app.route('/api/file', methods=['post'])
def process_file():
    global processing_file
    message = False
    points = 0
    processing_file = True
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filedir = path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filedir)
        message = True
        points = format_file(filedir)
    response = make_response(jsonify({
        "message": message, "points": points
    }), 200)
    response.headers["Content-Type"] = "application/json"
    processing_file = False
    return response


app.run(debug=False, port=port, host='0.0.0.0')
