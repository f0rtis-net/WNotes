from datetime import datetime
from werkzeug.utils import secure_filename
import os
"""
File structure:

date: %Y-%m-%d %H:%M
title: text <= 20 symbols
images: ["link1", "link2"] - later, bruh
body: text <= 300 symbols

"""

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def check_allowed(filename: str):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def image_work(request) -> str:
    if 'images' not in request.files:
        return

    image = request.files['images']
    if image.filename == '':
        return

    if image and check_allowed(image.filename):
        filename = secure_filename(image.filename)
        image.save(os.path.join('static\\images', filename))
        return f"/static/images/{filename}"
    
    return ""


def create_note(request) -> str:
    title = request.form.get('title')
    if not title or len(title) > 20: return "Title is too big or not exist!"

    image_path = image_work(request=request)

    body = request.form.get('body')
    if len(body) > 300: return "Note is too big!"

    #construct file fill
    file_data = f"date: \"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\"\n"
    file_data += f"title: {title}\n"

    if not image_path == "":
        file_data += f"image: {image_path}\n"

    file_data += body

    with open(f"content/notes/{file_data.__hash__()}.md", "w") as f:
        f.write(file_data)

    return "OK"