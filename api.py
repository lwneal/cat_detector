import flask
import json
import time
import tempfile
import subprocess
import cat_detector

MAX_IMAGE_LENGTH = 1024 ** 3

app = flask.Flask(__name__, static_url_path='/static/')

@app.route('/')
def index():
    return flask.send_from_directory('static', 'index.html')


@app.route('/check')
def health_check():
    return "OK"


@app.route('/<path:path>')
def host_static_file(path):
    return flask.send_from_directory('static', path)


def get_suffix(filename):
    if '.' in filename:
        return '.' + filename.split('.')[-1]
    return ''

@app.route('/cat_picture', methods=['POST'])
def upload_cat_picture():
    uploaded_file = flask.request.files.get('file')
    if not uploaded_file:
        flask.abort(400)
    with tempfile.NamedTemporaryFile(suffix=get_suffix(uploaded_file.filename)) as tmp:
        save_file(tmp, flask.request.files.get('file'))
        with tempfile.NamedTemporaryFile(suffix='.jpg') as tmp_converted:
            sanitize_image(tmp.name, tmp_converted.name)
            index = cat_detector.classify(cat_detector.convert_image(tmp_converted.name))
            message = cat_detector.is_it_a_cat(index)
    print('Returning message: {}'.format(message))
    response = {
        'class': 'cat',
        'message': message,
    }
    return flask.Response(json.dumps(response, indent=4), mimetype='application/json')


def sanitize_image(input_filename, output_filename):
    cmd = ['ffmpeg', '-y', '-i', input_filename, '-f', 'mjpeg', '-frames', '1', output_filename]
    print('Running command: {}'.format(' '.join(cmd)))
    subprocess.check_call(cmd)


def save_file(tmpfile, upload):
    if upload.content_length > MAX_IMAGE_LENGTH:
        flask.abort(400)
    upload.save(tmpfile.name)


if __name__ == '__main__':
    app.run('0.0.0.0', port=8000, debug=True)
