import os
from PIL import Image
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
paths  = r"static/user_profile_photo"
fake_photo = "No_face.png"
def allowed_file(file_name):
    print(file_name)
    return file_name.split(".")[-1].lower() in ALLOWED_EXTENSIONS

def change_name(file_name,user_name):
    return f"{user_name}_{file_name}"

def fake(user_name,fake=fake_photo):
    with Image.open(fake_photo) as img:
        name = os.path.basename(fake_photo)
        newimage = os.path.join(paths,f"{user_name}_{name}")
        img.save(newimage)
        return newimage.split('\\')[-1]

    