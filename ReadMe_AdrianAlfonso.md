# Project Overview
    The goal of this project is to develop a system for managing household devices. The system will allow users to:
    - Register device information (name, category, make, model, purchase date, etc.)
    - Store documents related to the device (guaranty documents, receipts, etc.)
    - Add notes and other relevant details to the device
    - Quickly find a device.
    - Manage possible device categories
    This project aims to provide a centralized platform for tracking and managing household devices, making it easier for users to keep their device information organized.
    This project is a web application developed with Python and Flask

# Python packages used
    You can install all depedencies by runing the command: 'pip install -r requirements.txt'

    Below is the ist of packages used and how to install then individually
    flask    #pip install flask
    

# Instructions to use the program
    1 On the console make sure to point the directory to this project's root foolder. 
    2 On the console run python app.py
    3 Once you run the command, the console will show a list of http addreses that can be used to launch the web application. You can press control and click on the address suggested on the console. That will launch the web application in a browser.

# Project specific files and folders
    * app.py - This files initializes the flask web framework and registers all the possible routes that can be accessed in this web app.
    * directory 'templates' - In this directory you will find all the html templates that will be rendered. Each template contains the html/css/javascript code plus a special flask language called Jinja. Jinja language is responsible for making the content in the page 'dynamic'.
    * templates/base.html - This file is the base template for all pages. It contains the commonly used html across the site.
    * directory 'static' - In this directory you will find all the files that will be served statically, css, javascript, images, etc. 
    * directory 'business_rules' - In this directory/pakage you will find all of the classes related to the business rules of the project.
    * business_rules/device.py  - In the module device.py, you will find the class Device which represents the information of a single device. 
    * business_rules/device_manager.py - In the module device_manager, you will find a class Device_Manager that handles all the data access logic for a device: (Create, Update, Delete, List, Find ,etc)

