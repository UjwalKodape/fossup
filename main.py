from flask import Flask, render_template, request, redirect,session, url_for
from database import Database 
import os

app = Flask(__name__)
app.secret_key = "abc"


UPLOAD_FOLDER = './static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = Database()


#USER ROUTES ----------------------------------------------------------------------------------------------

@app.route('/')
def index():
    a = db.pageUpdate()
    b = db.all_data()

    return render_template('index.html',data=a,blogData=b)

 
@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/signup')
def signup():
    return render_template("signup.html")

@app.route('/signOut')
def signOut():
    session.clear()  # Clears all session data
    print("signout")
    return redirect(url_for('index'))

@app.route('/userDashboard')
def userDashboard():
    name = session['users']
    # likes = db.count_likes()
    blogs=db.count_blogs()
    return render_template("./afterlogin/afterlogin.html",name=name,blogs=blogs)

@app.route('/uploadBlog')
def uploadBlog():
    name = session['users']
    return render_template("./afterlogin/uploadBlog.html",name=name)

@app.route('/profile')
def profile():
    name = session['users']
    return render_template("./afterlogin/profile.html",name=name)

@app.route('/yourBlog')
def yourBlog():
    a = db.all_data()
    name = session['users']
    return render_template("./afterlogin/yourBlogs.html",data=a,name=name)
 
@app.route('/viewBlogs')
def viewBlogs():
    a = db.all_data()
    # for item in a:
    #    item.image_path = f"/uploads/{item.image_name}" 
    return render_template("./afterlogin/viewBlogs.html",data=a)

@app.route('/manageBlogs')
def manageBlogs():
    a = db.all_data()
    name = session['users']

    return render_template("./afterlogin/manageBlogs.html",data=a,name=name)

@app.route('/updateBlog/<int:id>')
def updateBlog(id):
    print(id)
    print(type(id))
    session['update_blog_data'] = id
    status,data = db.get_Blog_id(id)
    print(data,status)
    if status == True:
        return render_template("./afterlogin/updateBlog.html",data1=data)
    else:
        return redirect('/manageBlogs')

@app.route('/upd_blog_data', methods=['POST','GET'])
def upd_blog_data():
    ids = session['update_blog_data']
    print("session n alii id = ", ids)
    if request.method == 'POST':
        # id = int(request.form['id'])    
        caption = request.form['caption']
        description = request.form['description']
        print(ids, caption, description) 
        print(type(ids)) 
        if db.updates_blog_data(ids, caption, description) == True:
            return redirect('/manageBlogs')
        else:
            print("**************************Error************************")
            return redirect('/manageBlogs')


@app. route('/storeUser',methods=['POST','GET'])
def storeUser():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        pass1 = request.form['pass1']
        pass22 = request.form['pass2']
        

        if pass1 != pass22:
            msg = "Password not matched !!"
            img = "./static/img/cross1.png"             
        else:
            if db.storeuser(name,email,pass1) == True:
                msg = "Signup Successful !!"
                img = "./static/img/right-icon.png"
                return render_template("message.html",msg=msg,img=img)
            else:
                msg = "Signup Failed !!!"
            return render_template("message.html",msg=msg,img=img)
    else:
        return "Failed !!!"

@app.route('/checkUser', methods=['POST','GET'])
def checkUser():
    if request.method == 'POST':
        username = request.form['user']
        pass11 = request.form['pass11']
        print(username,pass11)
        if db.checkUser(username, pass11) == True:
            session['users'] = username
            # return render_template('afterlogin.html',name=username)
            return redirect('/userDashboard')
        else:
            return redirect("/signup")




from werkzeug.utils import secure_filename
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        try:
            author_name = request.form.get('author_name')
            date = request.form.get('date')
            caption = request.form.get('caption')
            description = request.form.get('description')
            image = request.files.get('image')

            if not all([author_name, date, caption, description, image]):
                return render_template('error.html', error="All fields are required."), 400

            if image and allowed_file(image.filename):
                filename = secure_filename(image.filename)
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

                # # Check if the image has already been uploaded
                # if image_path in db.uploaded_images:
                #     return render_template('error.html', error="Image already uploaded."), 400

                image.save(image_path)

                print(author_name, date, caption, description, image_path)
                print("*******************************************************************")
                if db.file_uplod(author_name, date, caption, description,image_path)==True:
                    print("*************************************************details saved successfully.")
                    # if db.img_path_up(image_path, author_name)==True:
                    #     print("***********************    *************************path uploded")
                    return redirect('/yourBlog')
                    # else:
                    #     print("Path not uploded")
                    #     return redirect(url_for('userDashboard'))
                else:
                    print("Error saving image details to the database.")
                    return render_template('error.html', error="Failed to save image details."), 500
            elif image:
                return render_template('error.html', error="Invalid file type. Allowed types are: png, jpg, jpeg, gif."), 400
            else:
                return render_template('error.html', error="No image file uploaded."), 400

        except Exception as e:
            print(f"An error occurred: {e}")
            return f"An error occurred: {e}", 500
    else:
        return redirect(url_for('index'))
#ADMIN ROUTES -------------------------------------------------------------------------------------------------

@app.route('/adminLogin')
def adminLogin():
    return render_template("./admin/adminLogin.html")

@app.route('/checkAdmin', methods=['POST','GET'])
def checkAdmin():
    if request.method == 'POST':
        username = request.form['user']
        pass11 = request.form['pass11']
        
        if username == 'admin@gmail.com' and pass11 == 'admin':
            return redirect("/admin")
        if db.checkMod(username, pass11) == True:
            return redirect("/moderator")
        else:
            return redirect("/")

@app.route('/admin')
def admin():
    data = db.count_users()
    mod=db.count_Mods()
    blogs=db.count_blogs()
    # likes=db.count_likes('author_name')
    return render_template("./admin/admin.html",data=data,mod=mod,blogs=blogs)

@app.route('/manageUsers')
def manageUsers():
    a = db.users()
    return render_template("./admin/manageUserss.html",data=a)

@app.route('/manageMod')
def manageMod():
    a = db.moderators()
    return render_template("./admin/manageMod.html",data=a)

# @app.route('/updatePage/<int:id>')
# def updatePage(id):
#     print(id)
#     status,data = db.get_id(id)
#     print(data,status)
#     if status == True:
#         return render_template("uploadBlog.html",data1=data)



# @app.route('/update/<id>')
# def update(id):
#     if db.updates(id):
#         print("User  deleted successfully!", "success")
#         return redirect("/manageUsers",)
#     else:
#         print("Failed to delete user.", "error")
#         return redirect("/manageUsers")

@app.route('/updateUser/<int:id>')
def updateUser(id):
    print(id)
    print(type(id))
    session['update_user_id'] = id
    status,data = db.get_id(id)
    print(data,status)
    if status == True:
        return render_template("./admin/updateUser.html",data1=data)
    else:
        return redirect('/manageUsers')



@app.route('/deleteBlog/<int:id>')
def deletee_blog(id):
    if db.delete_BLog(id):
        print("User  deleted successfully!", "success")
        return redirect("/manageBlogs")
    else:
        print("Failed to delete user.", "error")
        return redirect("/manageBlogs")

@app.route('/upd_user_data', methods=['POST','GET'])
def upd_user_data():
    ids = session['update_user_id']
    print("session n alii id = ", ids)
    if request.method == 'POST':
        # id = int(request.form['id'])    
        username = request.form['username']
        Email = request.form['Email']
        password = request.form['password']
        print(ids, username, Email, password) 
        print(type(ids)) 
        if db.updates_user_data(ids, username, Email, password) == True:
            return redirect('/manageUsers')
        else:
            print("**************************Error************************")
            return redirect('/manageUsers')
    
    # return redirect('/manageUsers')

    # if db.get_id(id):
    #     print("ID sapdli reee",id)
    # else:
    #     print("ID nai bhetli")

@app.route('/updatePage')
def updatePage():
    print()
    return render_template("./admin/updatePage.html")

#--------------------------------------------------------Update Data-----------------------------------------------------------------------------------
# @app.route('/updatePage/<int:id>')
# def updatePage(id):
#     print(id)
#     print(type(id))
#     session['update_user_id'] = id
#     status,data = db.get_page_id(id)
#     print(data,status)
#     if status == True:
#         return render_template("./admin/updatePage.html",data1=data)
#     else:
#         return redirect('/manageUsers')
    

# @app.route('/upd_page_data', methods=['POST','GET'])
# def upd_page_data():
#     ids = session['update_user_id']
#     print("session n alii id = ", ids)
#     if request.method == 'POST':
#         # id = int(request.form['id'])    
#         name = request.form['name']
#         Email = request.form['email']
#         phone = request.form['phone']
#         address = request.form['address']
#         print(ids,name, Email, phone, address) 
#         print(type(ids)) 
#         if db.updates_page_data(ids, name, Email, phone, address) == True:
#             return redirect('/manageUsers')
#         else:
#             print("**************************Error************************")
#             return redirect('/manageUsers')
#-----------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/delete/<int:u_id>')
def delete_user(u_id):
    if db.delete_data(u_id):
        print("User  deleted successfully!", "success")
        return redirect("/manageUsers")
    else:
        print("Failed to delete user.", "error")
        return redirect("/manageUsers")
    

#MODERATOR ROUTES----------------------------------------------------------------------------------------------
@app.route('/moderator')
def moderator(): 
    return render_template("./moderator/moderator.html")

@app.route('/updateBlogStatus/<int:id>')
def updateBlogStatus(id):
    db.upDateBlogStatus(id)
    a = db.all_data()
    return render_template("./moderator/modManageBlog.html",data=a)

@app.route('/modManageBlog')
def modManageBlog():
    a = db.all_data()
    return render_template("./moderator/modManageBlog.html",data=a)

@app.route('/modManageUser')
def modManageUser():
    a = db.users()
    return render_template("./moderator/modManageUser.html",data=a)

@app. route('/storeMod',methods=['POST','GET'])
def storeMod():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['Phnumber']
        passw = request.form['passw']
            
        if db.storeMod(name,email,phone,passw) == True:
            return redirect("/manageMod")
        else:
            return redirect("/manageMod")
    else:
        return "Failed !!!"

@app.route('/updateMod/<int:id>')
def updateMod(id):
    print(id)
    print(type(id))
    session['update_Mod_data'] = id
    status,data = db.get_Mod_id(id)
    print(data,status)
    if status == True:
        return render_template("./admin/updateMod.html",data1=data)
    else:
        return redirect('/manageUsers')

@app.route('/upd_Mod_data', methods=['POST','GET'])
def upd_Mod_data():
    ids = session['update_Mod_data']
    print("session n alii id = ", ids)
    if request.method == 'POST':
        # id = int(request.form['id'])    
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']
        print(ids,name,email, phone, password) 
        print(type(ids)) 
        if db.update_Mod_data(ids,name,email, phone, password) == True:
            return redirect('/manageMod')
        else:
            print("**************************Error************************")
            return redirect('/moderators')

@app.route('/deleteMod/<int:id>')
def deletee_Mod(id):
    if db.delete_Mod(id):
        print("User  deleted successfully!", "success")
        return redirect("/manageMod")
    else:
        print("Failed to delete user.", "error")
        return redirect("/manageMod")
#page-----------------------------------------------------------------------------------------------------------

@app. route('/pageData',methods=['POST','GET'])
def pageData():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone_number = request.form['number']
        address = request.form['address']
            
        if db.pageData(name,email,phone_number,address) == True:
            return redirect("/")
        else:
            return redirect("/")
    else:
        return "Failed !!!"
    

@app. route('/like/<int:id>')
def like(id):
    print("**************************",id)
    # print("**************************",l)
    db.likes(id)
    return redirect('/')

@app. route('/dl/<int:id>')
def dl(id):
    print("**************************",id)
    db.dis_like(id)
    return redirect('/')

@app.route('/comment/<int:comment_id>/<name_text>/<comment_text>')
def comment(comment_id, name_text, comment_text):
    print("********Comment--> ")
    print(f"Received comment ID: {comment_id}")
    print(f"received name from text: {name_text}")
    print(f"Received comment text: {comment_text}")
    if db.comm(comment_id, name_text, comment_text) == True:
        return redirect('/')
    else:
        print("errorr")
        return redirect('/')


    # if request.method == 'POST':
    #     name = request.form['name']
    #     email = request.form['email']
    #     phone_number = request.form['number']
    #     address = request.form['address']
            
    #     if db.pageData(name,email,phone_number,address) == True:
    #         return redirect("/")
    #     else:
    #         return redirect("/")
    # else:
    #     return "Failed !!!"

# @app.route('/pageUpdate')
# def pageUpdate():
    
#     return render_template("index.html",data=a)

# @app. route('/view')
# def view():
#     a = db.all_data()
#     return render_template("yourBlogs.html",data=a)

if __name__ == '__main__':
    app.run(debug=True)