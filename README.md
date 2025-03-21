# IT Team's Project
# *Learning Space*
# Group 9
URL of web application
```
https://learningspace.pro/
```
### The Python version should be above *3.10*

## How to start the project
### 1. clone project
```bash
git clone https://github.com/porridgexj/learning_space.git
```
### 2. install requirements
```bash
pip install -r requirements.txt
```
### 3. run server
```bash
python manage.py runserver
```
### Set database
This project use MySQL as database.<br>
Create *.env* file in the root directory (where *manage.py* is)<br>
*(.env file is included in the ZIP source code file uploaded to Moodle)*<br>
Content of *.env* file should be like this
```
DB_NAME=my_database
DB_USER=my_user
DB_PASSWORD=my_secure_password
DB_HOST=localhost
DB_PORT=5432
```
# Project structure
```
\---learning_space
    +---space        # urls, views, models and unit test of space
    +---static       # css, js and images files
    +---templates    # html templates
    +---user         # urls, views, models and unit test of user
    +---urls.py      # urls of web page
    +---views.py     # views of web page
```
