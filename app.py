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
@app.route('/')
def starting_page ():
 flash("Done" , "danger")

 return render_template('starting_page.html')

@app.route('/Register' , methods = ['GET' , 'POST'])
@limiter.limit("10 per minute")

def Register () :
   if request.method == 'POST' :
      username = escape( request.form['username'])
      password = escape(request.form['password'])
      credit_card = escape(request.form['credit_card'])
      balance = int(escape(request.form['balance']))
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
         database.add_user(connection,username,password,credit_card,photo.filename,balance)
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
             if username == "admin" :
               return redirect(url_for('main_admin'))  # to do
             else :
               return redirect(url_for('shopping'))  # to do
           else :
               flash("Password does not match", "danger")
               return render_template('Login.html')
       else :
            flash("Invalid username", "danger")
            return render_template('Login.html')
    else :
       return render_template('Login.html')
    
@app.route('/logout')
def logout():
   session.pop('username',None)
   return redirect(url_for('starting_page'))       #to do  

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

           photo = request.files.get('prodpic')
           product_name = escape( request.form['prodname'])
           quantity = int(escape(request.form['prodquan']))
           price = int(escape(request.form['prodprice']))
         

           if photo :
              if not utils.allowed_file_size(photo):
                 flash("Unallowed size" , "danger")
                 return render_template('addProd.html')
              if not utils.allowed_file(photo.filename):
                flash("Unallowed extention" , "danger")
                return render_template('addProd.html')
        
           product=database.get_product(connection,product_name)  


           if product :
              total_quantity =product[2]+quantity
              database.add_product(connection,product_name,price,total_quantity,photo.filename)

           else :
              database.add_product(connection,product_name,price,quantity,photo.filename)
      
           photo.save(os.path.join(app.config['UPLOAD_FOLDER'],photo.filename))
           return redirect(url_for('main_admin'))
        
        else :
           flash("Unauthorized", "danger")
           return redirect(url_for('shopping'))
           
      
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
              #database.clear_comment(connection,product_name)
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


@app.route('/searchprod', methods=['GET', 'POST'])    # search for product
@limiter.limit("10 per minute")
def searchprod():
        if 'username' in session :

          product_name = escape(request.args.get('product_name'))
          products = database.search_product(connection, product_name)
          return render_template('shopping.html', products=products, product_name=product_name) ## to do :check
        
        else :
           flash("You must login first","danger")
           return redirect(url_for('Login'))  
         


@app.route('/add_comment', methods=['GET', 'POST'])     #add comment
@limiter.limit("10 per minute")
def add_comment():
  comments=None
  comments=database.show_all_comments(connection)

  if request.method == 'POST': 
      x = escape(request.form['comment']) 
      username=session.get('username')

      if username:
       database.Comment(connection,x)
       comments=database.show_all_comments(connection)
       return render_template('add_comment.html',comments=comments)
  
      else :
       flash("Please Login First", "danger")
       return redirect(url_for('Login'))  
  
  return render_template('add_comment.html',comments=comments)



#@app.route('/show_products', methods=['GET', 'POST'])   #show all products
#@limiter.limit("10 per minute")
#def show_products():
       # products = database.get_product(connection)
       # return render_template('search.html', products=products)

#@app.route('/show_products', methods=['GET', 'POST'])   #show specific products
#@limiter.limit("10 per minute")
#def show_products():
       #product_name = escape(request.args.get('product_name'))
       # products = database.get_product(connection,product_name)
       # return render_template('search.html', products=products, product_name=product_name)


@app.route('/shopping' , methods = ['GET' , 'POST'])
@limiter.limit("10 per minute")
def shopping () :
    products=None
    products = database.get_all_products(connection)
    
    if request.method=='POST':
      name=request.form.get('prodname')
      price = request.form.get('prodprice')

      if 'username' not in session:
        flash("You must be logged in to add items to your cart.", "warning")
        return redirect(url_for('Login'))
      else :
        
        session['correct_mac']=utils.create_mac(price)
        product = database.get_product(connection,name)
        return redirect(url_for('checkout', 
                            product_name=product[1], 
                            product_price=product[2], 
                            product_quantity=product[3],
                            product_id=product[0]))
      
    else :
       return render_template('shopping.html', products=products)

@app.route('/checkout', methods=['GET', 'POST'])
@limiter.limit("10 per minute")
def checkout():
    if request.method == 'POST':
       
        price = request.form.get('prodprice')
        Possible_Correct_MAC = utils.create_mac(price)

        if 'correct_mac' in session and session['correct_mac'] == Possible_Correct_MAC:
            username = session['username']
            user = database.get_user(connection,username)
            userbalance = user[5]
            if price > userbalance :
                flash("Purchase Failed, your balance is not enough")
                return redirect(url_for('shopping'))
            else :
               current_balance = userbalance - price
               database.update_user(connection,username, current_balance) 
               #quanedit
               flash(f"Purchase confirmed at price ${price}.")
               return redirect(url_for('shopping'))
        else:
            
            return f"Purchase Failed!!"
        
    product_name = request.args.get('prodname')
    product_price = request.args.get('prodprice')
    product_id = request.args.get('product_id')

    return render_template('checkout.html', 
                           product_name=product_name, 
                           product_price=product_price, 
                           product_id=product_id)

if __name__ == '__main__' :
    database.user_tb(connection)
    database.comment_tb(connection)
    database.product_tb(connection)
    app.run(debug=True)