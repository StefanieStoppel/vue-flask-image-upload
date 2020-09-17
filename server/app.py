import os
import argparse
import json
import re
import threading
import time
from datetime import datetime

from flask import Flask, jsonify, request, render_template, send_file
from flask_cors import cross_origin
from werkzeug.utils import secure_filename

UPLOAD_PATH = ''
FILE_EXT_PNG = ".png"
FILE_EXT_MAT = ".mat"
ALLOWED_EXTENSIONS = [FILE_EXT_PNG, FILE_EXT_MAT]
ALLOWED_FILE_SUFFIXES = ['-color.png', '-depth.png', '-meta.mat']
FRAME_ID_REGEX = r'\d{6}'
KEY_CLASS_ID = 'class_id'
KEY_CLASS_NAME = 'class_name'
KEY_FILE_NAMES = 'file_names'
KEY_FRAME_ID = 'frame_id'
PCD_SUFFIX = '_pred_cloud-completed.pcd'
VIEW_PCD_URL = 'http://localhost:5000/view-pcd'

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


def wait_for_pc_creation_until_timeout(pc_file_paths, timeout_seconds=100):
    print(f'Waiting {timeout_seconds} for final point cloud completion...')
    event = threading.Event()
    start_time = datetime.now()
    while True:
        event.wait(timeout=2)
        files_at_upload_path = [os.path.join(UPLOAD_PATH, file) for file in os.listdir(UPLOAD_PATH)
                                if os.path.isfile(os.path.join(UPLOAD_PATH, file))]
        all_pc_created = all(pc_file_path in files_at_upload_path for pc_file_path in pc_file_paths)
        if all_pc_created:
            print('All point clouds have been created and found...')
            return True
        if (datetime.now() - start_time).total_seconds() > timeout_seconds:
            print(f'Timeout of {timeout_seconds} exceeded. Aborting...')
            return False


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/view-pcd/<file_name>", methods=["GET"])
@cross_origin(origin=["localhost:5000", "localhost:8080"])
def view_pcd(file_name):
    print(f'Checking whether filename {file_name} exists...')
    pc_path = os.path.join(UPLOAD_PATH, file_name)
    if not os.path.isfile(pc_path):
        return jsonify(False), 500
    print('Returning point cloud file...')
    return send_file(pc_path)


@app.route("/upload-files", methods=["POST"])
@cross_origin(origin=["localhost:5000", "localhost:8080"])
def upload_files():
    files_per_frame_dict = dict()
    if request.files:
        files_per_frame_dict = create_files_per_frame_dict()
    if request.form:
        config_list = create_config_list(files_per_frame_dict)
        final_pc_file_paths = []
        for frame_config in config_list:
            frame_id = frame_config[KEY_FRAME_ID]
            final_pc_file_paths.append(os.path.join(UPLOAD_PATH, f'{frame_id}{PCD_SUFFIX}'))
            save_config_as_json(frame_config, frame_id)
            save_uploaded_files(files_per_frame_dict, frame_id)
        # wait 60 seconds while checking for the creation of the pc files every 2 seconds
        result = wait_for_pc_creation_until_timeout(final_pc_file_paths)
        if result is False:
            return jsonify(False)
        print('Returning URLs to fetch .pcd files from...')
        final_pc_file_urls = [fp.replace(UPLOAD_PATH, VIEW_PCD_URL) for fp in final_pc_file_paths]
        return jsonify(final_pc_file_urls), 200
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
