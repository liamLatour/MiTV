import imghdr
import time
from io import BytesIO
from os import getcwd, listdir
from os.path import isdir, isfile, join, basename, splitext, dirname, exists
from pathlib import Path
import random

from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from PIL import Image, ImageOps
from werkzeug.utils import secure_filename

from image_metadata import Videos, db_interface

# run with: waitress-serve --host 127.0.0.1 --port=5000 --threads=12 api_server:app

ref_path = join(getcwd(), "temp_people_ref")

if not exists(ref_path):
    ref_path = join(getcwd(), "people_ref")

root_photos_path = join(getcwd(), "photos")

app = Flask(__name__)
CORS(app)

db_interface.watch()

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
        save_path = join(join(getcwd(), "uploadDir"), association + '-' + event_name)
        Path(save_path).mkdir(parents=True, exist_ok=False)
        db_interface.add_folder_info(save_path, event_name, association)
        
        for file in request.files:
            f = request.files[file]
            f.save(join(save_path, secure_filename(f.filename)))
        
        return "File uploaded successfully"

@app.route("/upload_ref", methods=["GET", "POST"])
def upload_ref():
    if request.method == "POST":        
        uuid = request.form["uuid"]
        
        f = request.files["file"]
        img_path = join(ref_path, secure_filename(f.filename))
        f.save(img_path)
        
        # Add uuid to .people
        db_interface.add_reference_uuid(img_path, uuid)
        
        return "File uploaded successfully"

@app.route("/update/<path:dirname>", methods=["GET", "POST"])
def update(dirname):
    if request.method == "POST":
        # Check if it has the right to
        if request.json["login"] not in allowed_cookies:
            return "Vous n'etes pas connecter"

        db_interface.update_folder_info(dirname, request.json["metaData"])
        
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

@app.route("/get_by_uuid/<uuid>")
def get_photos_uuid(uuid):
    media = db_interface.get_reference_uuid(uuid, request.args.get("path"))

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
    return send_file(join(dirname(filename), Videos.small_dir_name, splitext(basename(filename))[0]) + ".mp4", mimetype="video/mp4")

@app.route("/vdownload/<path:filename>")
def get_download_vmedia(filename):
    return send_file(filename, mimetype="video/webm")

@app.route("/download/<path:filename>")
def get_download_media(filename):
    return send_file(filename, mimetype="image/jpeg")

# Architecture
@app.route("/architecture/<path:dirname>")
def get_architecture(dirname):
    t = time.time()
    
    media = db_interface.get_folder_info(dirname)
    media = media | db_interface.get_folder_representation(dirname)

    print("Response time", time.time()-t)
    return media

if __name__ == "__main__":
    app.run()
