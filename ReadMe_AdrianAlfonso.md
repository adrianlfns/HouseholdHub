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
    You can install all dependencies by running the command: 'pip install -r requirements.txt'

    Below is the ist of packages used and how to install then individually
    flask    #pip install flask
    

# Instructions to use the program
    1 On the console make sure to point the directory to this project's root folder. 
    2 On the console run the command 'python app.py'
    3 Once you run the command, the console will show a list of http addresses that can be used to launch the web application. You can press control and click on the address suggested on the console. That will launch the web application in a browser.

# Project specific files and folders
    * app.py - This files initializes the flask web framework and registers all the possible routes that can be accessed in this web app.
    * directory 'templates' - In this directory you will find all the html templates that will be rendered. Each template contains the html/css/javascript code plus a special flask language called Jinja. Jinja language is responsible for making the content in the page 'dynamic'.
    * templates/base.html - This file is the base template for all pages. It contains the commonly used html across the site.
    * directory 'static' - In this directory you will find all the files that will be served statically, css, javascript, images, etc. 
    * directory 'business_rules' - In this directory/package you will find all of the classes related to the business rules of the project.
    * business_rules/entity_base.py - In the module entity_base, you will find a class EntityBase class which is a base class for other classes such as Device and Category. This little class contains the property ID which is common for Devices and Categories and also another common method which is to_dictionary
    * business_rules/device.py  - In the module device.py, you will find the class Device which represents the information of a single device. 
    * business_rules/device_manager.py - In the module device_manager, you will find a class Device_Manager that handles all the data access logic for a device: (Create, Update, Delete, List, Find ,etc)
    * business_rules/category.py -In the module category.py, you will find the class Category which represents the information of a single category.
    * business_rules/categories_manager.py - In the module categories_manager, you will find a class Categories_Manager that handles all the data access logic for a category: (Create, Update, Delete, List, Find ,etc)
    * business_rules/category_count.py - In this module, there is a class named CategoryCount that is using for holding statistics about categories. For now it only holds the category name/ category id and the device count that is under a category. 
    * business_rules/expiration_types_lookup.py - In this module we can find a class named ExpirationTypeLookup that defines the IDs fo the possible device expiration types. It also exposes functionality that can be done with the possible expiration types. 

