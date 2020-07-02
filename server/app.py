import os

from pathlib import Path
from flask import Flask, jsonify, request
from flask_cors import cross_origin
from werkzeug.utils import secure_filename

ALLOWED_FILETYPES = ["image/png"]
HOME = str(Path.home())
DESTINATION_PATH = os.path.abspath(os.path.join(HOME, "Desktop/vue-flask-image-upload"))

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)


@app.route("/upload-images", methods=["POST"])
@cross_origin(origin="localhost:8080")
def upload_images():
    if request.files:
        for i, file in enumerate(request.files):
            try:
                image = request.files[f"images[{i}]"]
                if image.content_type not in ALLOWED_FILETYPES:
                    return jsonify("Unsupported Media Type"), 415
                if not os.path.exists(DESTINATION_PATH):
                    os.makedirs(DESTINATION_PATH, exist_ok=True)
                image.save(os.path.join(DESTINATION_PATH, secure_filename(image.filename)))
            except (KeyError, FileNotFoundError):
                return jsonify("An error occurred while processing the file."), 500
        return jsonify("Images saved."), 200
    return jsonify(False)


if __name__ == "__main__":
    app.run()
