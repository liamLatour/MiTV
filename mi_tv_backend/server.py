from flask import Flask, send_file, jsonify, send_from_directory, render_template, request
from flask_cors import CORS
from io import BytesIO 
from os import listdir
from os.path import isfile, join, isdir, abspath
import imghdr
import json
from PIL import Image, ImageOps
from get_faces_of import GetFaces
from get_groups_of import GetGroups

# run with: waitress-serve --host 127.0.0.1 --port=5000 --threads=12 server:app

app = Flask(__name__, template_folder="web")
CORS(app)
root_photos_path = "C:\\Users\\liaml\\Projets\\ROOTS Template\\mi_tv_backend\\photos"
media_per_page = 5000
get_faces = GetFaces()

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


# Serves flutter app

@app.route('/')
def render_page_web():
    return render_template('index.html')

@app.route('/<path:name>')
def return_flutter_doc(name):
    return send_from_directory("web", name)

# Serve media

def serve_pil_image(pil_img):
    img_io = BytesIO()
    pil_img.save(img_io, 'JPEG', quality=90)
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
    image = ImageOps.exif_transpose(image)
    image = image.resize((500, round(image.size[1]/(image.size[0]/500))),Image.Resampling.NEAREST)
    
    return serve_pil_image(image) #send_file(filename, mimetype='image/png')

@app.route('/media/<path:filename>')
def get_media(filename):

    return send_file(filename, mimetype='image/png')

@app.route('/architecture/<path:dirname>')
def get_architecture(dirname):
    media = {
        "files": []
    }
    groups = GetGroups(dirname)
    page_nb = 1 if request.args.get('page_nb')==None else request.args.get('page_nb')
    page_nb = int(page_nb)
    i = 0
    
    for f in listdir(dirname):
        i += 1
        if i < (page_nb-1)*media_per_page:
            continue
        if i >= page_nb*media_per_page:
            break
    
        path = join(dirname, f)
        media_data = {
            "path": path,
        }
        if isfile(path):
            if imghdr.what(path) == "jpeg" and groups.is_not_in_group(path):
                media_data["type"] = "pic"
                media_data["is_portrait"] = False#is_portrait(path)
            elif f != ".meta" and f != ".people": #TODO: check if it is really a video
                media_data["type"] = "vid"
        elif isdir(path):
            media_data["type"] = "dir"
            media_data = add_dir_info(path, media_data)
        
        if "type" in media_data:
            media["files"].append(media_data)
    
    # Global info on dir
    media = add_dir_info(dirname, media)

    response = jsonify(media)
    return response

#TODO: Maybe put that in metadata for faster access
def is_portrait(path):
    image = Image.open(path)
    image = ImageOps.exif_transpose(image)
    return image.size[1] > image.size[0]

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