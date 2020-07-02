import os

from pathlib import Path
from flask import Flask, jsonify, request, render_template
from flask_cors import cross_origin
from werkzeug.utils import secure_filename

FILE_EXT_PNG = ".png"
FILE_EXT_MAT = ".mat"
ALLOWED_EXTENSIONS = [FILE_EXT_PNG, FILE_EXT_MAT]
HOME = str(Path.home())
DESTINATION_PATH = os.path.abspath(os.path.join(HOME, "Desktop/vue-flask-image-upload"))

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
# app = Flask(__name__,
#             static_folder="./static",
#             template_folder="./static")
app.config.from_object(__name__)

#
# @app.route('/')
# def index():
#     return render_template("index.html")


@app.route("/upload-files", methods=["POST"])
@cross_origin(origin="localhost:8080")
def upload_images():
    if request.files:
        for i, file in enumerate(request.files):
            try:
                file = request.files[f"files[{i}]"]
                _, file_extension = os.path.splitext(file.filename)
                if file_extension not in ALLOWED_EXTENSIONS:
                    return jsonify("Unsupported file type"), 415
                if not os.path.exists(DESTINATION_PATH):
                    os.makedirs(DESTINATION_PATH, exist_ok=True)
                file.save(os.path.join(DESTINATION_PATH, secure_filename(file.filename)))
            except (KeyError, FileNotFoundError):
                return jsonify("An error occurred while processing the file."), 500
        return jsonify("Files saved."), 200
    return jsonify(False)


if __name__ == "__main__":
    app.run()
