from flask import Flask,Blueprint,render_template,redirect,request,flash,url_for,current_app,flash
from mongodb import *
from werkzeug.utils import secure_filename
from file_manager import allowed_file,change_name,fake_photo,fake
import os

from bson import ObjectId
main = Blueprint('main',__name__)




@main.route("/",methods=['GET','POST'])
def home():
    All_contact = contact.find()
    no_of_contact = contact.count_documents({})
    return render_template("home.html",All_contact=All_contact,no_of_contact=no_of_contact)

@main.route('/search',methods=['POST'])
def search():
    name = request.form.get("name")
    if contact.find_one({"Name":name}):
        contacts = contact.find({"Name":name})
        return render_template("home.html",All_contact=contacts)
    else:
        flash("Not found","error")
    return redirect(url_for("main.home"))



@main.route("/create/",methods=['GET','POST'])
def create_contact():
    photo = None
    if request.method == 'POST':
        name = request.form.get("name")
        phone_no = request.form.get("phone_no")      
        photo = request.files.get("profile_photo")  
        
        if photo.filename == "":
            photo_name = fake(name)
        
        elif allowed_file(photo.filename):
            photo_name = secure_filename(change_name(photo.filename,name))
            path = current_app.config.get('UPLOAD_FOLDER')
            photo.save(os.path.join(path,photo_name))
        else:
            return redirect(url_for("main.create_contact"))    
        
        contact.insert_one({"Name": name, "Phone No": phone_no,"Photo":photo_name})
        return redirect(url_for("main.home"))

            
    
    return render_template("create_contact.html")

@main.route("/profile/<id>")
def profile(id):
    contacts = contact.find_one({"_id":ObjectId(id)})
    return render_template("profile_view.html",contact=contacts)


@main.route("/update/<id>",methods=['GET','POST'])
def update(id):
    if request.method == 'POST':
        name = request.form.get("name")
        phone_no = request.form.get("phone_no")
        photo = request.files.get("profile_photo")
        
        if contact.find_one({'_id':ObjectId(id)}):
            if allowed_file(photo.filename):
                delete_old_photo(id)
                photo_name = secure_filename(photo.filename)
                path = current_app.config.get('UPLOAD_FOLDER')
                photo.save(os.path.join(path,photo_name))
                flash("Successfully Added","success")
                contact.update_one({"_id":ObjectId(id)},{'$set':{"Name":name,"Phone No":phone_no,"Photo":photo_name}})
            else:
                flash("Successfully Added","success")
                contact.update_one({"_id":ObjectId(id)},{'$set':{"Name":name,"Phone No":phone_no}})
            return redirect(url_for("main.profile",id=ObjectId(id)))
    
    old_info = contact.find_one({'_id':ObjectId(id)})    
    return render_template('update_contact.html',old_info=old_info)



@main.route("/delete/<id>")
def delete(id):
    delete_old_photo(id)
    contact.delete_one({"_id":ObjectId(id)})
    flash("Successfully Deleted","success")
    return redirect(url_for("main.home"))