from flask import Flask, request
from cis_requests import *
from waitress import serve
from werkzeug.utils import secure_filename

app = Flask(__name__)
XTIKA_CUTOFF = 10

@app.route('/record_schedule_prediction', methods=['POST'])
def record_schedule_prediction():
    file = request.files.get('file')
    if file:
        filename = secure_filename(file.filename)
        extension = filename.split('.')[-1]
        text = tika(file)
        if extension == 'pdf' and len(text) < XTIKA_CUTOFF:
            text = xtika(file)
        text = nlp_buddy_analyze(text)['summary']
        prediction = deep_detect_classify(text)
        return {'prediction': prediction}
    else:
        return {'error': 'No file found.'}

if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=8000)
