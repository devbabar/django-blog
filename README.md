# django-blog
A complete blogging application with user authentication and authorization, dashboard, comments and responsive design.

# features:
* Blog home page where users can see all the blogs, login and logout options. 
* Users can only view the limited details of each blog. For advance features like to create post and comment on any post, they must need to register and login.
* Register new user, login and logout sessions. The Django authentication system is being used handles both authentication and authorization.
* @Login_required decoraters is being used to only allowed logged in users to view dashboard, create post and comment.
* Custom dashboard for each user to create and view draft and future date posts.
* Django messaging framework to display custom messages.
* A dynamic search engine which used optimized query sets “Q” to filter from title, content, user’s first and last names. If no match found, it will display a message "Sorry No Result Found, Try Again..!”.
* Custom navbar to stay visible on scrolldown and back to the top button to get back to the top.
* Slide in effects on scrolldown from left to right.
* Responsive design for any screensize.
* Scalable pagination to display only three post at single page with navigation bar.

# Steps to run:

### Step 1:
Create a folder.

$ mkdir django_blog

Create a virtual enviroment.

$pip install virtualenv

$ cd django_blog

$ virtualenv env

$ source env/bin/activate

### Step 2:
Install requirements.txt

$pip install -r requirements.txt

### Step 3:
Edit settings.py with database credentials.

<p align="center">
  <img src="src/screenshots/db_con.png" width="600px" height="200px">
</p>

### Step 4:
Database migrations.

$ python manage.py makemigrations

$ python manage.py migrate

### Step 5:
Run project.

$ python manage.py runserver

### Folder Structure.
<p align="center">
  <img src="src/screenshots/folder_structure.png" width="300px" height="700px">
</p>

### User table in database.
<p align="center">
  <img src="src/screenshots/user_db.png" width="700px" height="200px">
</p>

### Comments table in database.
<p align="center">
  <img src="src/screenshots/comment_db.png" width="700px" height="200px">
</p>

# ---------------------------- Demo -------------------------------
#### Home page
http://127.0.0.1:8000/posts/ is a home page which displays all posts posted by the user. This page also display options to login, register, search, pagination to next 3 post. Users can only see the post image, title, date, author name and first few lines of the post. To view the whole post and comment, user must login or register. 
<p align="center">
  <img src="src/screenshots/welcome_page.png" width="700px" height="400px">
</p>

#### Responsive Navbar.
On scroll down, navbar will change its position and moves down along the page
<p align="center">
  <img src="src/screenshots/nav_down.png" width="700px" height="400px">
</p>

#### Login
Django authentication framework is being used to validate the username and password and perform login, logout operations. If either of it is wrong, it will prompt a custom error message. On success, it will show a custom messages. It will also give an option to register if user is not registered yet.
<p align="center">
  <img src="src/screenshots/login.png" width="600px" height="300px">
</p>

Error if username or password is not corrent.
<p align="center">
  <img src="src/screenshots/login_error.png" width="600px" height="300px">
</p>

#### Register.
Register a new user and validate their credentials. If the username is already exists or password is not is correct, it will display an error messages. Form validation is been used to check whether both password fields must for the successful registration.
<p align="center">
  <img src="src/screenshots/register.png" width="600px" height="300px">
</p>
Error message if username is already exists.
<p align="center">
  <img src="src/screenshots/register_validation.png" width="600px" height="300px">
</p>
Error message if both password fields doesn't match.
<p align="center">
  <img src="src/screenshots/password_not_same.png" width="600px" height="300px">
</p>

#### Dashboard
Once user is been authorized, it will redirect to custom dashboard. This displays all posts related to the current logged in user. In addition to this, it will also display three options which are draft, future and create post. Each section displays related contents.
<p align="center">
  <img src="src/screenshots/dashboard.png" width="700px" height="300px">
</p>
Onclick, display related content.
<p align="center">
  <img src="src/screenshots/dashboard_options.jpg" width="800px" height="400px">
</p>
Create post calendar using JQueryui datepicker.
<p align="center">
  <img src="src/screenshots/calender.png" width="600px" height="300px">
</p>

#### Comment.
A dynamic commenting functionality enable users to comment at any post once they successfully logged in. Ajax is been used to handle comments without refreshing the page.
<p align="center">
  <img src="src/screenshots/comment_bx.png" width="800px" height="400px">
</p>
