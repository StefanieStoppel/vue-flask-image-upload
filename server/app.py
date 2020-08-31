import os
import argparse
import json
import re

from flask import Flask, jsonify, request, render_template, send_file
from flask_cors import cross_origin
from werkzeug.utils import secure_filename

FILE_EXT_PNG = ".png"
FILE_EXT_MAT = ".mat"
ALLOWED_EXTENSIONS = [FILE_EXT_PNG, FILE_EXT_MAT]
ALLOWED_FILE_SUFFIXES = ['-color.png', '-depth.png', '-meta.mat']
FRAME_ID_REGEX = r'\d{6}'
KEY_CLASS_ID = 'class_id'
KEY_CLASS_NAME = 'class_name'
KEY_FILE_NAMES = 'file_names'
KEY_FRAME_ID = 'frame_id'

# configuration
DEBUG = True

# instantiate the flask app
app = Flask(__name__, static_folder="./static", template_folder="./static")


def save_uploaded_files(files_per_frame_dict, frame_id):
    for file in files_per_frame_dict[frame_id]:
        filepath = os.path.join(UPLOAD_PATH, secure_filename(file.filename))
        print(f"Saving file to {filepath}")
        file.save(filepath)


def save_config_as_json(frame_config, frame_id):
    save_filename = secure_filename(f"{frame_id}-config.json")
    with open(os.path.join(UPLOAD_PATH, save_filename), "w") as frame_config_file:
        json.dump(frame_config, frame_config_file)


def create_config_list(files_per_frame_dict):
    ycb_object_class = json.loads(request.form["objectClass"])
    return [
        {KEY_FRAME_ID: frame_id,
         KEY_FILE_NAMES: [file.filename for file in file_list],
         KEY_CLASS_ID: ycb_object_class["value"],
         KEY_CLASS_NAME: ycb_object_class["displayName"]}
        for frame_id, file_list in files_per_frame_dict.items()]


def create_files_per_frame_dict():
    files_per_frame_dict = dict()
    for _, file in request.files.items():
        try:
            if not has_valid_file_extension(file) and has_valid_file_suffix(file):
                continue
            frame_id = find_frame_id(file.filename)
            if frame_id not in files_per_frame_dict:
                files_per_frame_dict[frame_id] = list()
            files_per_frame_dict[frame_id].append(file)
        except ValueError as error:
            print(f"ERROR: {error}")
    return files_per_frame_dict


def has_valid_file_extension(file):
    _, file_extension = os.path.splitext(file.filename)
    result = file_extension in ALLOWED_EXTENSIONS
    if not result:
        print(f"ERROR: File name {file.filename} doesn't have correct file extension.")
    return result


def has_valid_file_suffix(file):
    result = any(suffix in file.filename for suffix in ALLOWED_FILE_SUFFIXES)
    if not result:
        print(f"ERROR: File name {file.filename} doesn't contain correct suffix.")
    return result


def find_frame_id(filename: str) -> str:
    matches = re.match(FRAME_ID_REGEX, filename)
    if not bool(matches):
        raise ValueError(f"The file {filename} does not belong to the YCB Video dataset.")
    return matches[0]


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/view-pcd", methods=["GET"])
@cross_origin(origin="localhost:5000")
def view_pcd():
    return send_file('/Users/sstoppel/dev/Uni/vue-file-upload/client/src/components/models/pcd/binary/037_scissors.pcd', attachment_filename='037_scissors.pcd')


@app.route("/upload-files", methods=["POST"])
@cross_origin(origin="localhost:5000")
def upload_images():
    files_per_frame_dict = dict()
    if request.files:
        files_per_frame_dict = create_files_per_frame_dict()
    if request.form:
        config_list = create_config_list(files_per_frame_dict)
        for frame_config in config_list:
            frame_id = frame_config[KEY_FRAME_ID]
            save_config_as_json(frame_config, frame_id)
            save_uploaded_files(files_per_frame_dict, frame_id)
        return jsonify("Files saved."), 200
    return jsonify(False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--upload_path', type=str, required=True,
                        help='Path to upload files to which are provided via the web interface.')
    args = parser.parse_args()
    UPLOAD_PATH = args.upload_path
    if not os.path.exists(UPLOAD_PATH):
        os.makedirs(UPLOAD_PATH, exist_ok=True)
    app.run(host="0.0.0.0", port="5000")

