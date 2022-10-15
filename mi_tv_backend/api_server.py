from flask import Flask, send_file, jsonify
from flask_cors import CORS
from io import BytesIO 
from os import listdir, getcwd
from os.path import isfile, join, isdir
import imghdr
import json
from PIL import Image, ImageOps
from image_metadata import GetGroups, GetOrientation, GetFaces
import time

# run with: waitress-serve --host 127.0.0.1 --port=5000 --threads=12 api_server:app

app = Flask(__name__)
CORS(app)
root_photos_path = join(getcwd(), "photos")
get_faces = GetFaces(join(getcwd(), "people_ref"))

"""
Return structure for media is:
    if 'dir':
        "path": {
            "type": "dir",
            "thumbnail": path/to/thumbnail,
            "exlude_thumbnail": "false"/"true",
            "event_name": "Photos",
            "association": "cercle"
        }
    elif 'pic' or 'vid':
        "path": {
            "type": "pic"/"vid"
        }

This way metadata is easy to add without breaking anything
"""

# Serve media

def serve_pil_image(pil_img, quality=90):
    img_io = BytesIO()
    pil_img.save(img_io, 'JPEG', quality=quality)
    img_io.seek(0)
    
    return send_file(img_io, mimetype='image/jpeg')

@app.route('/get_by_id/<id>')
def get_photos_id(id):
    media = {
        "files": []
    }
    
    for img in get_faces.get_face_by_id(id):
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

@app.route('/get_by_name/<name>')
def get_photos_name(name):
    media = {
        "files": []
    }
    
    for img in get_faces.get_face_by_name(name):
        media["files"].append(
            {
                "path": img[0],
                "type": "pic",
                "closeness": img[1]["closeness"],
            }
        )

    media["event_name"] = "Photo de " + name.capitalize()
    media["association"] = "IA"

    return jsonify(media)

#TODO: only for images for now
@app.route('/media_low_res/<path:filename>')
def get_media_low_res(filename):
    image = Image.open(filename)
    image = image.resize((500, round(image.size[1]/(image.size[0]/500))),Image.Resampling.NEAREST)
    image = ImageOps.exif_transpose(image)
    
    return serve_pil_image(image)

@app.route('/media/<path:filename>')
def get_media(filename):
    image = Image.open(filename)
    image = image.resize((2250, round(image.size[1]/(image.size[0]/2250))),Image.Resampling.LANCZOS)
    image = ImageOps.exif_transpose(image)
    
    return serve_pil_image(image, 100) #send_file(filename, mimetype='image/png')

@app.route('/download/<path:filename>')
def get_download_media(filename):
    return send_file(filename, mimetype='image/png')

@app.route('/architecture/<path:dirname>')
def get_architecture(dirname):
    t = time.time()
    media = {
        "files": []
    }

    orientation = GetOrientation(dirname)
    groups = GetGroups(dirname)
    
    for f in listdir(dirname):
        path = join(dirname, f)
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
            media["files"].append(media_data)
    
    # Global info on dir
    media = add_dir_info(dirname, media)

    response = jsonify(media)
    print("Response time", time.time()-t)
    return response

def add_dir_info(path, meta):
    with open(join(path, ".meta"), 'r', encoding='utf-8') as file:
        data = json.load(file)
        for label in data:
            if label == "thumbnail":
                meta[label] = join(path, data[label])
            else:
                meta[label] = data[label]
    return meta

if __name__ == '__main__':
    app.run()