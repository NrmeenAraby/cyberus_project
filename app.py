from flask import Flask, render_template, request, redirect, url_for, session, flash 
from markupsafe import escape
import database
import os
import utils
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
connection = database.connect()
app.secret_key = "SUPER-SECRET"
limiter = Limiter(app=app, key_func=get_remote_address,
                  default_limits=["50 per minute"], storage_uri="memory://")

@app.route('/Register' , methods = ['GET' , 'POST'])
@limiter.limit("10 per minute")
##
def Register () :
   if request.method == 'POST' :
      username = escape( request.form['username'])
      password = escape(request.form['password'])
      credit_card = escape(request.form['credit_card'])
      photo = request.files.get('profile_picture')

      if not utils.is_strong_password(password) :
         flash( "Weak Password, Please Choose a stronger one", "danger")
         return render_template('Register.html')
      if photo :
         if not utils.allowed_file_size(photo):
            flash("Unallowed size" , "danger")
            return render_template('Register.html')
         if not utils.allowed_file(photo.filename):
            flash("Unallowed extention" , "danger")
            return render_template('Register.html')
         
      user = database.get_user(connection,username)
      if user :
         flash("allready exist, Enter another one" , "danger")
         return render_template('Register.html')
      else :
         database.add_user(connection,username,password,credit_card,photo.filename)
         photo.save(os.path.join(app.config['UPLOAD_FOLDER'],photo.filename))
         return redirect(url_for('Login'))   
   return render_template('Register.html')
         
      


@app.route('/Login' , methods = ['GET' , 'POST'])
@limiter.limit("10 per minute")
def Login () :
    if request.method == 'POST' :
       username = escape(request.form['username'])
       password = escape(request.form['password'])

       user = database.get_user(connection , username)  

       if user :
           if utils.is_password_match(password , user[2]):
             session['username'] = username
            #  if username == "admin" :
            #    return redirect(url_for('admin_main'))  # to do
            #  else :
            #   return redirect(url_for('shopping'))  # to do
           else :
               flash("Password does not match", "danger")
               return render_template('Login.html')
       else :
            flash("Invalid username", "danger")
            return render_template('Login.html')
    else :
       return render_template('Login.html')
    
# @app.route('/logout')
# def logout():
#    session.pop('username',None)
#    return redirect(url_for('home'))       #to do  

@app.route('/main_admin' , methods = ['GET' , 'POST'])
def main_admin () :
   flash("Password does not match", "danger")
   return render_template('main_admin.html')

@app.route('/addProd' , methods = ['GET' , 'POST'])
@limiter.limit("10 per minute")
def addProd () :
   if request.method == 'POST' :
    
     if 'username' in session:
     
        if session['username'] == 'admin':

           product_name = escape( request.form['prodname'])
           quantity = escape(request.form['prodquan'])
           price = escape(request.form['prodprice'])
           photo = request.files.get('profile_picture')

           if photo :
              if not utils.allowed_file_size(photo):
                 flash("Unallowed size" , "danger")
                 return render_template('addProd.html')
              if not utils.allowed_file(photo.filename):
                flash("Unallowed extention" , "danger")
                return render_template('addProd.html')
        
           product=database.get_product(connection,product_name)  


           if product :
              total_quantity =product[3]+quantity
              database.add_product(connection,product_name,price,total_quantity,photo.filename)

           else :
              database.add_product(connection,product_name,price,quantity,photo.filename)
      
           photo.save(os.path.join(app.config['UPLOAD_FOLDER'],photo.filename))
           return redirect(url_for('main_admin'))
        
        else :
           flash("Unauthorized", "danger")
           return redirect(url_for('Login')) ## to do : redirect to shopping page
           
      
     else :
         flash("Please Login First", "danger")
         return redirect(url_for('Login'))  
        
   return render_template('addProd.html')

@app.route('/delProd' , methods = ['GET' , 'POST'])
@limiter.limit("10 per minute")
def delProd () :
   if request.method == 'POST' :
      
       if 'username' in session:
     
           if session['username'] == 'admin':

             product_name = escape( request.form['prodname'])
   
             product=database.get_product(connection,product_name)  

             if product :
              database.delete_product(connection,product_name)

             else :
              flash("Product is not exist", "danger")
        
      
             return redirect(url_for('main_admin'))
           
           else :
             flash("Unauthorized", "danger")
             return redirect(url_for('Login')) ## to do : redirect to shopping page
           
       else :
            flash("Please Login First", "danger")
            return redirect(url_for('Login'))  
          
              

   return render_template('delProd.html')


if __name__ == '__main__' :
    database.user_tb(connection)
    app.run(debug=True)