import imghdr
import time
from io import BytesIO
from os import getcwd
from os.path import join, basename, splitext, dirname, exists
from pathlib import Path
import random

from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from PIL import Image, ImageOps
from werkzeug.utils import secure_filename

from flasgger import Swagger

from image_metadata import Videos, db_interface

# run with: waitress-serve --host 127.0.0.1 --port=5000 --threads=12 api_server:app

ref_path = join(getcwd(), "people_ref")

root_photos_path = join(getcwd(), "photos")

app = Flask(__name__)
swagger = Swagger(app)
CORS(app)

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

@app.route("/upload", methods=["POST"])
def upload_files():
    """
    Upload some files to the drive via the front-end.
    ---
    parameters:
      - name: login
        in: cookie
        type: string
        format: uuid
        required: true
        description: Login cookie.
      - name: event_name
        in: formData
        type: string
        required: True
        description: Name of the event associated with the media files.
      - name: association
        in: formData
        type: string
        required: True
        description: Name of the association who made the medias.
      - name: files
        in: formData
        type: array
        required: True
        items:
          type: file
        description: Medias to upload (Werkzeug FileStorage objects).

    produces:
      text/plain

    responses:
      200:
        description: Query has been processed (upload can have worked, or not).
        schema:
          type: string
          example: File uploaded successfully
    """
    if request.method == "POST":
        # Check if it has the right to
        if request.form["login"] not in allowed_cookies:
            return "Vous n'êtes pas connecté."
        
        event_name = request.form["event_name"]
        association = request.form["association"]
        save_path = join(join(getcwd(), "uploadDir"), association + '-' + event_name)
        Path(save_path).mkdir(parents=True, exist_ok=False)
        db_interface.add_folder_info(save_path, event_name, association)
        
        for file in request.files:
            f = request.files[file]
            f.save(join(save_path, secure_filename(f.filename)))
        
        return "File uploaded successfully"

@app.route("/upload_ref", methods=["POST"])
def upload_ref():
    """
    Upload a facial reference to the back-end via the front.
    ---
    parameters:
      - name: uuid
        in: header
        type: string
        required: true
        description: UUID for the picture (to store and reference in DB).
      - name: file
        in: formData
        type: file
        required: True
        description: Reference picture to upload (Werkzeug FileStorage object).

    produces:
      text/plain

    responses:
      200:
        description: Upload result (failed/succeeded).
        schema:
          type: string
          example: File uploaded successfully
    """
    if request.method == "POST":        
        uuid = request.form["uuid"]
        
        f = request.files["file"]
        img_path = join(ref_path, secure_filename(f.filename))
        f.save(img_path)
        
        # Add uuid to .people
        db_interface.add_reference_uuid(img_path, uuid)
        
        return "File uploaded successfully"

@app.route("/update/<path:dirname>", methods=["POST"])
def update(dirname):
    """
    Update the preview image of a folder.
    ---
    parameters:
      - name: path
        in: path
        type: string
        required: true
        description: Path to the media.
      - name: dirname
        in: path
        type: string
        required: true
        description: The media folder location.
      - name: login
        in: cookie
        type: apiKey
        required: true
        description: Login cookie.
      - name: metaData
        in: header
        type: string
        required: true
        description: String-dumped JSON containing the picture's metadata.

    produces:
      text/plain

    responses:
      200:
        description: Upload result (failed/succeeded).
        schema:
          type: string
          example: File uploaded successfully
    """
    if request.method == "POST":
        # Check if it has the right to
        if request.json["login"] not in allowed_cookies:
            return "Vous n'êtes pas connecté."

        db_interface.update_folder_info(dirname, request.json["metaData"])
        db_interface.update_folder_representation(Path(dirname).parent.absolute())
        
        return "File updated successfully"

@app.route("/login", methods=["POST"])
def login():
    """
    Login as admin.
    ---
    parameters:
      - name: username
        in: formData
        type: string
        required: true
        description: Admin username
      - name: password
        in: formData
        type: string
        required: true
        description: Admin password (yes it's barbarism to send it in plain but this is temporary)

    responses:
      200:
        description: A cookie containing either a "UUID" atesting for privilege or "False".
        schema:
          type: object
          properties:
            res:
              type: string
              format: uuid
              example: 14995851753388834
    """
    if request.method == "POST":
        username = request.json["username"]
        password = request.json["password"]
        
        if username == "admin" and password == "pass":
            allowed_cookies.append(str(random.random())[2:])
            return {"res": allowed_cookies[-1]}
        return {"res": False}

@app.route("/disconnect", methods=["GET", "POST"])
def disconnect():
    """
    Disconnect (from admin account).
    ---
    produces:
      text/plain

    responses:
      200:
        description: Whether disconnection was successful or not.
        schema:
          type: string
          example: Not logged in
    """
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
    """
    Gets all photos for a given reference picture's UUID.
    ---
    parameters:
      - name: uuid
        in: path
        type: string
        format: uuid
        required: true
        description: Reference photo UUID.

    responses:
      200:
        description: Media files close to the reference photo.
        schema:
          type: object
          properties:
            files:
              properties:
                path:
                  type: string
                  example: photos/perm/IMG_13.jpg
                closeness:v
                  type: number
                  format: float
                  example: 0.87
                type:
                  type: string
                  example: pic
    """
    media = db_interface.get_reference_uuid(uuid, request.args.get("path"))

    media["event_name"] = "Mes Photos"
    media["association"] = "IA"

    return jsonify(media)

@app.route("/media_low_res/<path:filename>")
def get_media_low_res(filename):
    """
    Gets a picture's preview image.
    ---
    parameters:
      - name: path
        in: path
        type: string
        required: true
        description: Path to the media.
      - name: filename
        in: path
        type: string
        required: true
        description: The name of the media.

    produces:
      file

    responses:
      200:
        description: File (Werkzeug FileStorage object) containing the preview image.
    """
    if splitext(basename(filename))[1][1:] in Videos.supported_formats:
        filename = join(dirname(filename), Videos.small_dir_name, splitext(basename(filename))[0]) + ".jpg"

    image = Image.open(filename)
    image = image.resize((500, round(image.size[1]/(image.size[0]/500))),Image.Resampling.NEAREST)
    image = ImageOps.exif_transpose(image)
    
    return serve_pil_image(image)

@app.route("/media/<path:filename>")
def get_media(filename):
    """
    Gets a resized picture.
    ---
    parameters:
      - name: path
        in: path
        type: string
        required: true
        description: Path to the media.
      - name: filename
        in: path
        type: string
        required: true
        description: The name of the media.

    produces:
      file

    responses:
      200:
        description: File (Werkzeug FileStorage object) containing the resized image.
    """
    image = Image.open(filename)
    image = image.resize((2250, round(image.size[1]/(image.size[0]/2250))),Image.Resampling.LANCZOS)
    image = ImageOps.exif_transpose(image)
    
    return serve_pil_image(image, 100)

@app.route("/vmedia/<path:filename>")
def get_vmedia(filename):
    """
    Gets a compressed video.
    ---
    parameters:
      - name: path
        in: path
        type: string
        required: true
        description: Path to the media.
      - name: filename
        in: path
        type: string
        required: true
        description: The name of the media.

    produces:
      file

    responses:
      200:
        description: File (Werkzeug FileStorage object) containing the compressed video.
    """
    return send_file(join(dirname(filename), Videos.small_dir_name, splitext(basename(filename))[0]) + ".mp4", mimetype="video/mp4")

@app.route("/vdownload/<path:filename>")
def get_download_vmedia(filename):
    """
    Gets a video.
    ---
    parameters:
      - name: path
        in: path
        type: string
        required: true
        description: Path to the media.
      - name: filename
        in: path
        type: string
        required: true
        description: The name of the media.

    produces:
      file

    responses:
      200:
        description: File (Werkzeug FileStorage object) containing the video.
    """
    return send_file(filename, mimetype="video/webm")

@app.route("/download/<path:filename>")
def get_download_media(filename):
    """
    Gets a full size picture.
    ---
    parameters:
      - name: path
        in: path
        type: string
        required: true
        description: Path to the media.
      - name: filename
        in: path
        type: string
        required: true
        description: The name of the media.

    produces:
      file

    responses:
      200:
        description: File (Werkzeug FileStorage object) containing the image.
    """
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
