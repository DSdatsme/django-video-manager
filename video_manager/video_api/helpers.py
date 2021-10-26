

# core dependencies
import subprocess
import json
from pathlib import Path
import os

# django dependencies
from video_manager.constants import SERVER_DOMAIN
from django.core.files.storage import default_storage

def get_video_data(filename):
    cmnd = " ".join(['ffprobe', '-show_format', '-loglevel',  'quiet','-print_format', 'json', filename])
    p = subprocess.Popen(cmnd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out, err =  p.communicate()
    video_data = json.loads(out.decode('utf-8'))
    print(filename)
    if err:
        print(err)
        raise Exception("Unable to get video metadata")
    return video_data

def make_video_url(path, name):
    """Make Video URL that can fetch the video directly
    """
    return "https://" + SERVER_DOMAIN +  "/videos/play/" + path + name

def get_video_metadata_response(video_obj):
    return {
                "id": video_obj.id,
                "video_name": video_obj.name,
                "size": video_obj.size,
                "path": video_obj.path,
                "duration": video_obj.duration,
                "codec": video_obj.codec,
                "container": video_obj.container,
                "playback_url": make_video_url(video_obj.path, video_obj.name)
            }

def get_field_value(field_name, request_obj):
    """Handle form requests that are in list form
    """
    field_value = request_obj.data.get(field_name, "")
    if isinstance(field_value, list):
        field_value = field_value[0]
    return field_value

def save_video_file(filepath, video):
    return default_storage.save(filepath, video)

def delete_video_file(filepath):
    return default_storage.delete(filepath)

def video_exists(filepath):
    print(filepath)
    print(default_storage.exists(filepath))
    return default_storage.exists(filepath)

def move_file(source_path, dest_path):
    Path("/".join(dest_path.split('/')[:-1]) + "/").mkdir(parents=True, exist_ok=True)        # create folder if it does not exists
    os.rename(source_path, dest_path)
