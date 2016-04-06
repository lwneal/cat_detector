import flask
import json
import time
import tempfile
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


@app.route('/cat_picture', methods=['POST'])
def upload_cat_picture():
    with tempfile.NamedTemporaryFile() as tmp:
        filename = save_file(tmp, flask.request.files.get('file'))
        index = cat_detector.classify(cat_detector.convert_image(tmp.name))
        message = cat_detector.is_it_a_cat(index)
    print('Returning message: {}'.format(message))
    response = {
        'class': 'cat',
        'message': message,
    }
    return flask.Response(json.dumps(response, indent=4), mimetype='application/json')


def save_file(tmpfile, upload):
    if upload.content_length > MAX_IMAGE_LENGTH:
        flask.abort(400)
    upload.save(tmpfile.name)


if __name__ == '__main__':
    app.run('0.0.0.0', port=8000, debug=True)
