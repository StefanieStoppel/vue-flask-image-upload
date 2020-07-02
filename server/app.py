import os
import argparse

from flask import Flask, jsonify, request, render_template
from flask_cors import cross_origin
from werkzeug.utils import secure_filename

FILE_EXT_PNG = ".png"
FILE_EXT_MAT = ".mat"
ALLOWED_EXTENSIONS = [FILE_EXT_PNG, FILE_EXT_MAT]

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__,
            static_folder="./static",
            template_folder="./static")
app.config.from_object(__name__)


@app.route('/')
def index():
    return render_template("index.html")


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
                if not os.path.exists(UPLOAD_PATH):
                    os.makedirs(UPLOAD_PATH, exist_ok=True)
                filepath = os.path.join(UPLOAD_PATH, secure_filename(file.filename))
                print(f"Saving file to {filepath}")
                file.save(filepath)
            except (KeyError, FileNotFoundError):
                return jsonify("An error occurred while processing the file."), 500
        return jsonify("Files saved."), 200
    return jsonify(False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--upload_path', type=str, required=True,
                        help='Path to upload files to which are provided via the web interface.')
    args = parser.parse_args()
    UPLOAD_PATH = args.upload_path
    app.run(host="0.0.0.0", port="5000")
