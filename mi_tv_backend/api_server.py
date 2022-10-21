import imghdr
import json
import time
from io import BytesIO
from os import getcwd, listdir
from os.path import isdir, isfile, join, basename, splitext, dirname, exists, abspath
from pathlib import Path
import random

from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from PIL import Image, ImageOps
from werkzeug.utils import secure_filename

from image_metadata import GetFaces, GetGroups, GetOrientation, UpdateMetadata, Videos, add_uuid

# run with: waitress-serve --host 127.0.0.1 --port=5000 --threads=12 api_server:app

ref_path = join(getcwd(), "temp_people_ref")

if not exists(ref_path):
    ref_path = join(getcwd(), "people_ref")

root_photos_path = join(getcwd(), "photos")

app = Flask(__name__)
CORS(app)
get_faces = GetFaces(ref_path)

default_meta = {
    "event_name": "Evenement",
    "association": "Aucune",
    "thumbnail": "photos/default.jpg",
    "exlude_thumbnail": "false"
}

# This is temp until fusion with portail-etu
allowed_cookies = []

"""
Return structure for media is:
    if "dir":
        "path": {
            "type": "dir",
            "thumbnail": path/to/thumbnail,
            "exlude_thumbnail": "false"/"true",
            "event_name": "Photos",
            "association": "cercle"
        }
    elif "pic" or "vid":
        "path": {
            "type": "pic"/"vid"
        }

This way metadata is easy to add without breaking anything
"""

# Upload media

@app.route("/upload", methods=["GET", "POST"])
def upload_files():
    if request.method == "POST":
        # Check if it has the right to
        if request.form["login"] not in allowed_cookies:
            return "Vous n'etes pas connecter"
        
        event_name = request.form["event_name"]
        association = request.form["association"]
        save_path = join(join(join(getcwd(), "uploadDir"), association), event_name)
        Path(save_path).mkdir(parents=True, exist_ok=False)
        
        for file in request.files:
            f = request.files[file]
            f.save(join(save_path, secure_filename(f.filename)))
        
        return "File uploaded successfully"

@app.route("/upload_ref", methods=["GET", "POST"])
def upload_ref():
    if request.method == "POST":        
        uuid = request.form["uuid"]
        
        f = request.files["file"]
        f.save(join(ref_path, secure_filename(f.filename)))
        
        # Add uuid to .people
        add_uuid(uuid, join(ref_path, secure_filename(f.filename)), join(ref_path, '.people'))
        
        return "File uploaded successfully"

@app.route("/update/<path:dirname>", methods=["GET", "POST"])
def update(dirname):
    if request.method == "POST":
        # Check if it has the right to
        if request.json["login"] not in allowed_cookies:
            return "Vous n'etes pas connecter"
        
        update_meta = UpdateMetadata(dirname)
        update_meta.update_metadata(request.json["metaData"])
        
        return "File updated successfully"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.json["username"]
        password = request.json["password"]
        
        if username == "admin" and password == "pass":
            allowed_cookies.append(str(random.random())[2:])
            return {"res": allowed_cookies[-1]}
        return {"res": False}

@app.route("/disconnect", methods=["GET", "POST"])
def disconnect():
    if request.method == "POST":
        login = request.json["login"]
        if login in allowed_cookies:
            allowed_cookies.remove(login)
            return "Logged out"
    return "Not logged in"

# Serve media
def serve_pil_image(pil_img, quality=90):
    img_io = BytesIO()
    if 'exif' in pil_img.info:
        pil_img.save(img_io, "JPEG", quality=quality, exif=pil_img.info['exif'])
    else:
        pil_img.save(img_io, "JPEG", quality=quality)
    img_io.seek(0)
    
    return send_file(img_io, mimetype="image/jpeg")

@app.route("/get_by_id/<id>")
def get_photos_id(id):
    media = {
        "files": []
    }
    
    for img in get_faces.get_face_by_id(int(id)):
        media["files"].append(
            {
                "path": img[0],
                "type": "pic",
                "closeness": img[1],
            }
        )

    media["event_name"] = "Photo de " + id
    media["association"] = "IA"

    return jsonify(media)

@app.route("/get_by_uuid/<uuid>")
def get_photos_uuid(uuid):
    media = {
        "files": []
    }
    
    path = abspath(request.args.get("path"))
    
    for img in get_faces.get_face_by_uuid(uuid, path):
        media["files"].append(
            {
                "path": img[0],
                "type": "pic",
                "closeness": img[1],
            }
        )

    media["event_name"] = "Mes Photos"
    media["association"] = "IA"

    return jsonify(media)

@app.route("/media_low_res/<path:filename>")
def get_media_low_res(filename):
    if splitext(basename(filename))[1][1:] in Videos.supported_formats:
        filename = join(dirname(filename), Videos.small_dir_name, splitext(basename(filename))[0]) + ".jpg"

    image = Image.open(filename)
    image = image.resize((500, round(image.size[1]/(image.size[0]/500))),Image.Resampling.NEAREST)
    image = ImageOps.exif_transpose(image)
    
    return serve_pil_image(image)

@app.route("/media/<path:filename>")
def get_media(filename):
    image = Image.open(filename)
    image = image.resize((2250, round(image.size[1]/(image.size[0]/2250))),Image.Resampling.LANCZOS)
    image = ImageOps.exif_transpose(image)
    
    return serve_pil_image(image, 100)

@app.route("/vmedia/<path:filename>")
def get_vmedia(filename):
    return send_file(join(dirname(filename), Videos.small_dir_name, splitext(basename(filename))[0]) + ".webm", mimetype="video/webm")

@app.route("/vdownload/<path:filename>")
def get_download_vmedia(filename):
    return send_file(join(dirname(filename), splitext(basename(filename))[0]) + ".webm", mimetype="video/webm")

@app.route("/download/<path:filename>")
def get_download_media(filename):
    return send_file(filename, mimetype="image/jpeg")

# Architecture
@app.route("/architecture/<path:dirname>")
def get_architecture(dirname):
    t = time.time()
    media = {
        "files": []
    }

    orientation = GetOrientation(dirname)
    groups = GetGroups(dirname)
    
    for f in listdir(dirname):
        path = join(dirname, f)

        if isdir(path) and Videos.small_dir_name in basename(f):
            continue

        media_data = {
            "path": path,
        }

        if isfile(path):
            if imghdr.what(path) == "jpeg":
                is_not_in_group, others = groups.is_not_in_group(path)
                if is_not_in_group:
                    media_data["type"] = "pic"
                    media_data["is_portrait"] = orientation.is_portrait(path)
                    media_data["others"] = others
                    media["files"].append(media_data)
            elif f != ".meta" and f != ".people": #TODO: check if it is really a video
                media_data["type"] = "vid"
                media["files"].append(media_data)
        elif isdir(path):
            media_data["type"] = "dir"
            media_data = add_dir_info(path, media_data)
            print(media_data)
            media["files"].append(media_data)
    
    # Global info on dir
    media = add_dir_info(dirname, media)

    response = jsonify(media)
    print("Response time", time.time()-t)
    return response

def add_dir_info(path, meta):
    meta_path = join(path, ".meta")
    if isfile(meta_path):
        with open(meta_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            for label in data:
                if label == "thumbnail" and data["thumbnail"] != "":
                    meta[label] = join(path, data[label])
                else:
                    meta[label] = data[label]
    
    # Add default config
    for key in default_meta:
        if key not in meta or meta[key] == "":
            meta[key] = default_meta[key]
    
    return meta

if __name__ == "__main__":
    app.run()
