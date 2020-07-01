import os

from flask import Flask, jsonify, request
from flask_cors import cross_origin
from werkzeug.utils import secure_filename

DESTINATION_PATH = os.path.abspath("/Users/sstoppel/Desktop/test")
ALLOWED_FILETYPES = ['image/png']

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)


@app.route('/upload-images', methods=['POST'])
@cross_origin(origin='localhost:8080')
def upload_images():
    if request.files:
        for i, file in enumerate(request.files):
            try:
                image = request.files[f"images[{i}]"]
                if image.content_type not in ALLOWED_FILETYPES:
                    return jsonify("Unsupported Media Type"), 415
                image.save(os.path.join(DESTINATION_PATH, secure_filename(image.filename)))
            except KeyError:
                return 500
        return jsonify("Images saved."), 200
    return jsonify(False)


if __name__ == '__main__':
    app.run()
