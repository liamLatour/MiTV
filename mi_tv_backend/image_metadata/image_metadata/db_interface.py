from os import getcwd
from os.path import isabs, isdir, relpath

import numpy as np
from pymongo import MongoClient, DESCENDING

client = MongoClient()

# Get database
db = client.mitv

# Get collection (equivalent to a table)
col_reference_meta = db.reference_meta  # stores uuid, image_path, seen_in
col_folders_meta = db.folders_meta      # stores event_name, association
col_ai_encoding = db.ai_encoding        # stores encodings for all images
col_ai_meta = db.ai_meta                # stores faces in image and groups

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
    occurrence = col_reference_meta.find_one({"uuid": uuid})
    
    media = {
        "files": []
    }
    
    if occurrence != None and "occurrence" in occurrence:
        for occ in occurrence["occurrence"]:
            if occ["seen_in"].startswith(path):
                media["files"].append({
                    "path": occ["seen_in"],
                    "closeness": occ["closeness"],
                    "type": "pic",
                })

    media["files"].sort(key= lambda x: x["closeness"])

    return media

def add_reference_uuid(img_path, uuid):
    path = sanitize_path(img_path)
    worked = col_reference_meta.find_one_and_update(
            {"path": path},
            {"$set": {
                "uuid": uuid,
                }
            })
    if not worked:
        col_reference_meta.insert_one({
            "path": path,
            "uuid": uuid,
        })
        
def add_reference_seen_in(img_path, seen_in_path, closeness):
    path = sanitize_path(img_path)
    seen_in = sanitize_path(seen_in_path)
    worked = col_reference_meta.find_one_and_update(
        {"path": path},
        {"$push": {
            "occurrence": {
                "seen_in": seen_in,
                "closeness": closeness,
                },
            }
        })
    if not worked:
        col_reference_meta.insert_one({
            "path": path,
            "occurrence": [{
                "seen_in": seen_in,
                "closeness": closeness,
            }],
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
    orientation = col_ai_meta.find_one({"path": path})
    
    if orientation == None or "is_portrait" not in orientation:
        return False
        
    return orientation["is_portrait"]

def get_groups_ai_meta(img_path):
    path = sanitize_path(img_path)
    groups = col_ai_meta.find_one({"path": path})
    
    if groups == None or "group_nb" not in groups:
        return (True, None)
        
    others = col_ai_meta.find({"group_nb": groups["group_nb"]})
    group = []
    
    for ot in others:
        group.append(ot["path"])
        
    return (not groups["hidden"], group)

def add_orientation_ai_meta(img_path, is_portrait):
    path = sanitize_path(img_path)
    worked = col_ai_meta.find_one_and_update(
            {"path": path},
            {"$set": {
                "is_portrait": is_portrait,
                }
            })
    if not worked:
        col_ai_meta.insert_one({
            "path": path,
            "is_portrait": is_portrait,
        })

def add_group_ai_meta(img_path, group_nb, hidden = True):
    path = sanitize_path(img_path)
    worked = col_ai_meta.find_one_and_update(
            {"path": path},
            {"$set": {
                "group_nb": group_nb,
                "hidden": hidden,
                }
            })
    if not worked:
        col_ai_meta.insert_one({
            "path": path,
            "group_nb": group_nb,
            "hidden": hidden,
        })

def add_ai_meta(img_path, faces):
    path = sanitize_path(img_path)
    worked = col_ai_meta.find_one_and_update(
            {"path": path},
            {"$set": {
                "faces": faces,
                }
            })
    if not worked:
        col_ai_meta.insert_one({
            "path": path,
            "faces": faces,
        })

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
    path = sanitize_path(img_path)
    worked = col_ai_encoding.find_one_and_update(
            {"path": path},
            {"$set": {
                "encoding_version": encoding_version,
                "encoding": np.array(encoding).tolist()
                }
            })
    if not worked:
        col_ai_encoding.insert_one({
            "path": path,
            "encoding_version": encoding_version,
            "encoding": np.array(encoding).tolist(),
        })

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
}
"""

default_folder_meta = {
    "thumbnail": "photos/default.jpg",
    "exclude_thumbnail": False,
    "event_name": "Evenement",
    "association": "Aucune",
}

def get_folder_info(folder_path):
    path = sanitize_path(folder_path)
    info = col_folders_meta.find_one({"path": path}, {"path": 0, "_id":0})
    if info == None:
        return default_folder_meta
    
    if info["thumbnail"] == "":
        info["thumbnail"] = default_folder_meta["thumbnail"]
    
    return info

def update_folder_info(folder_path, update):
    path = sanitize_path(folder_path)
    col_folders_meta.find_one_and_update({"path": path}, {"$set": update})

def add_folder_info(folder_path, event_name, association, thumbnail=None, exclude_thumbnail=None):
    if thumbnail == None:
        thumbnail = default_folder_meta["thumbnail"]
        
    if exclude_thumbnail == None:
        exclude_thumbnail = default_folder_meta["exclude_thumbnail"]
    
    col_folders_meta.insert_one({
        "path": sanitize_path(folder_path),
        "thumbnail": thumbnail,
        "exclude_thumbnail": exclude_thumbnail,
        "event_name": event_name,
        "association": association,
    })


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