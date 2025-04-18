## Project Management API/BACKEND

This project is being built with one goal in mind, streamline project management. From creating projects , to handling project membership, to allowing project admins to be able to assign tasks to members as well as facilitating file sharing among members within the same project; this is what this Api is all about. Hopefully i will integrate real time chat service into it soon.

## features

1. Account creation,logging in and authentication using jwt
-An admin can create an account for himself with all admin priveleges 
-He can then create account for project memebers using email provided by members to be
- where a project member forgets his account password ,admin can reset that for him/her based on the email provided

2. Admin is able to do the following;
- create, delete and update project details
-assign members to project-
-assign tasks to memebrs in the project
-An admin is also a member of the project, automatically
-assign admin priveleges to other users,
- No admin can delete a project created by another admin or delete a user from that project.

3. members in the project can do the following;
- view other members in the project,
-view tasks assigned specifically to them

- share files among eachother in the project


## installation

- create a folder in your editor
-pull this repository into your folder
-create a python virtual environment using cmd terminal ( use ## : python -m venv venv)
- activate the virtual environment
-install all the packages and dependencies in the requirements.txt file 
(use ##: pip install -r requirements.txt )
- run application in terminal using (## : uvicorn App.main:app)

 voilaaa 

you can reach me on whatsapp or call +233 202160514 if you have further questions.


