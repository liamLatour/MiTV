import imghdr
from os import getcwd, listdir
from os.path import basename, isabs, isdir, isfile, join, relpath

import checksumdir
import numpy as np
from bson.json_util import dumps, loads
from pymongo import DESCENDING, MongoClient

from .vid_handler import Videos

client = MongoClient()

# Get database
db = client.mitv

# Get collection (equivalent to a table)
col_reference_meta = db.reference_meta  # stores uuid, image_path, seen_in
col_folders_meta = db.folders_meta      # stores event_name, association
col_ai_encoding = db.ai_encoding        # stores encodings for all images
col_ai_meta = db.ai_meta                # stores faces in image and groups

# If not enough add groups data to folders_meta
col_reference_meta.create_index([("uuid", DESCENDING)])
col_folders_meta.create_index([("path", DESCENDING)])
col_ai_encoding.create_index([("path", DESCENDING)])
col_ai_meta.create_index([("path", DESCENDING)])


## col_reference_meta
"""
{
    path: string,           # path is relative
    uuid: string,
    occurrence: array,
}
"""

def get_reference_uuid(uuid, base_path):
    path = sanitize_path(base_path)
    print(path)
    occurrence = col_reference_meta.find_one({"uuid": uuid}, {"_id":0})
    
    media = {
        "files": []
    }
    
    if occurrence != None and "occurrence" in occurrence:
        for occ in occurrence["occurrence"]:
            if occ["seen_in"].startswith(path):
                #TODO: currently not handling portrait images
                media["files"].append({
                    "path": occ["seen_in"],
                    "closeness": occ["closeness"],
                    "type": "pic",
                })

    media["files"].sort(key= lambda x: x["closeness"])

    return media

def add_reference_uuid(img_path, uuid):
    add_data_safely(col_reference_meta, img_path, {"uuid": uuid})
        
def add_reference_seen_in(img_path, seen_in_path, closeness):
    path = sanitize_path(img_path)
    seen_in = sanitize_path(seen_in_path)
    
    worked = col_reference_meta.find_one_and_update(
        {"path": path},
        {"$push": {
            "occurrence": {
                "seen_in": seen_in,
                "closeness": closeness
            }
        }
    })
    if not worked:
        col_reference_meta.insert_one({
            "path": path,
            "occurrence": [{
                "seen_in": seen_in,
                "closeness": closeness
            }]
        })

def remove_reference_seen_in(img_path, seen_in_path):
    path = sanitize_path(img_path)
    seen_in = sanitize_path(seen_in_path)
    col_reference_meta.find_one_and_update(
        {"path": path},
        {"$pull": {
            "occurrence": {
                "seen_in": seen_in,
                },
            }
        })

## col_ai_meta
"""
{
    path: string,           # path is relative
    faces: array,
    is_portrait: bool,
    group_nb: int,
    hidden: bool,
}
"""

def get_orientation_ai_meta(img_path):
    path = sanitize_path(img_path)
    orientation = col_ai_meta.find_one({"path": path}, {"_id":0})
    
    if orientation == None or "is_portrait" not in orientation:
        return False
        
    return orientation["is_portrait"]

def get_groups_ai_meta(img_path):
    path = sanitize_path(img_path)
    groups = col_ai_meta.find_one({"path": path}, {"_id":0})
    
    if groups == None or "group_nb" not in groups:
        return (True, None)
        
    others = col_ai_meta.find({"group_nb": groups["group_nb"]})
    group = []
    
    for ot in others:
        group.append(ot["path"])
        
    return (not groups["hidden"], group)

def add_orientation_ai_meta(img_path, is_portrait):
    add_data_safely(col_ai_meta, img_path, {"is_portrait": is_portrait})

def add_group_ai_meta(img_path, group_nb, hidden = True):
    add_data_safely(col_ai_meta, img_path, {"group_nb": group_nb, "hidden": hidden})

def add_ai_meta(img_path, faces):
    add_data_safely(col_ai_meta, img_path, {"faces": faces})

def get_ai_meta(img_path):
    path = sanitize_path(img_path)    
    return col_ai_meta.find_one({"path": path}, {"path": 0, "_id":0})


## col_ai_encoding
"""
{
    path: string,           # path is relative
    encoding_version: int,
    encoding: array,
}
"""

def add_ai_encoding(img_path, encoding_version, encoding):
    data = {"encoding_version": encoding_version, "encoding": np.array(encoding).tolist()}
    add_data_safely(col_ai_encoding, img_path, data)

def get_ai_encoding(img_path):
    path = sanitize_path(img_path)
    data = col_ai_encoding.find_one({"path": path}, {"path": 0, "_id":0})
    if data == None:
        return None
    
    data["encoding"] = np.array(data["encoding"])
    
    return data

## col_folders_meta
"""
{
    path: string,           # path is relative
    thumbnail: string,
    exclude_thumbnail: bool,
    event_name: string,
    association: string,
    hash: string,
    representation: object,
}
"""

default_folder_meta = {
    "thumbnail": "photos/default.jpg",
    "exclude_thumbnail": False,
    "event_name": "Evenement",
    "association": "Aucune",
}

def get_folder_representation(folder_path):
    path = sanitize_path(folder_path)
    representation = col_folders_meta.find_one({"path": path}, {"_id":0})
    
    if representation == None or "representation" not in representation:
        update_folder_representation(folder_path)
        representation = col_folders_meta.find_one({"path": path}, {"_id":0})
        
    return loads(representation["representation"])

def update_folder_representation(folder_path):
    media = {
        "files": []
    }
    
    for f in listdir(folder_path):
        path = join(folder_path, f)

        media_data = {
            "path": path,
        }

        if isfile(path):
            if imghdr.what(path) == "jpeg":
                is_not_in_group, others = get_groups_ai_meta(path)
                if is_not_in_group:
                    media_data["type"] = "pic"
                    media_data["is_portrait"] = get_orientation_ai_meta(path)
                    media_data["others"] = others
                    media["files"].append(media_data)
            elif Videos.is_supported(path):
                media_data["type"] = "vid"
                media["files"].append(media_data)
        elif isdir(path) and Videos.small_dir_name not in basename(f):
            media_data["type"] = "dir"
            media_data = media_data | get_folder_info(path)
            media["files"].append(media_data)
    
    if media != {"files": []}:
        add_data_safely(col_folders_meta, folder_path, {"representation": dumps(media)})

def update_folders_hash(folder_paths):
    for path in folder_paths:
        update_folder_hash(path)
    
def update_folder_hash(folder_path):
    path = sanitize_path(folder_path)
    update_folder_representation(folder_path)
    add_data_safely(col_folders_meta, folder_path, {"hash": checksumdir.dirhash(path)})

def get_folder_info(folder_path):
    path = sanitize_path(folder_path)
    info = col_folders_meta.find_one({"path": path}, {"_id":0, "representation":0, "hash":0})
    if info == None or "event_name" not in info:
        info = default_folder_meta
    
    if "thumbnail" not in info or info["thumbnail"] == default_folder_meta["thumbnail"]:        
        info["thumbnail"] = get_thumbnail(folder_path)
        add_data_safely(col_folders_meta, folder_path, info)
    
    return info

def update_folder_info(folder_path, update):
    add_data_safely(col_folders_meta, folder_path, update)
    update_folder_representation(folder_path)

def add_folder_info(folder_path, event_name, association, thumbnail=None, exclude_thumbnail=False):
    if thumbnail == None:
        thumbnail = get_thumbnail(folder_path)
    
    data = {
        "path": sanitize_path(folder_path),
        "thumbnail": thumbnail,
        "exclude_thumbnail": exclude_thumbnail,
        "event_name": event_name,
        "association": association,
    }
    add_data_safely(col_folders_meta, folder_path, data)
    update_folder_representation(folder_path)

# Utilities

def sanitize_path(path):
    san = path
    if isabs(san):
        san = relpath(san, getcwd())
    san = san.replace("\\", "/")
    san = san.replace("//", "/")
    
    if isdir(san) and san[-1] != "/":
        san = san + "/"
    
    return san

def get_thumbnail(folder_path):
    for f in listdir(folder_path):
        _path = sanitize_path(join(folder_path, f))
        if isfile(_path) and imghdr.what(_path) == "jpeg":
            return _path
    return default_folder_meta["thumbnail"]

def add_data_safely(collection, path, data, method="$set"):
    path = sanitize_path(path)
    worked = collection.find_one_and_update({"path": path},{method: data})
    if not worked:
        collection.insert_one({"path": path}|data)
        
def folder_changed(folder_path):
    path = sanitize_path(folder_path)
    folder_hash = col_folders_meta.find_one({"path": path}, {"_id":0})
    
    if folder_hash == None or "hash" not in folder_hash:
        return True
    
    return checksumdir.dirhash(folder_path) != folder_hash["hash"]

def recalculate_all_folders():
    folders = col_folders_meta.find()
    
    for folder in folders:
        update_folder_representation(folder["path"])
