# gudlift-registration

![Gudlft logo](https://user.oc-static.com/upload/2020/09/22/16007798203635_P9.png "Gudlft logo")

Why:
---


This is a proof of concept (POC) project to show a light-weight version of our competition booking platform. The aim is the keep things as light as possible, and use feedback from the users to iterate.

Getting Started:
---

This project uses the following technologies:

* Python v3.x+

* [Flask](https://flask.palletsprojects.com/en/1.1.x/)

    Whereas Django does a lot of things for us out of the box, Flask allows us to add only what we need. 
     

* [Virtual environment](https://virtualenv.pypa.io/en/stable/installation.html)

    This ensures you'll be able to install the correct packages without interfering with Python on your machine.

    Before you begin, please ensure you have this installed globally. 


Installation:
---

- After cloning, change into the directory and type <code>virtualenv venv</code> or <code>pyhton -m virtualenv venv</code>. This will then set up a a virtual python environment within venv directory.

- Next, type <code>source venv/bin/activate</code> on UNIX or <code> venv/Scripts/activate</code> on Windows. You should see that your command prompt has changed to the name of the folder. This means that you can install packages in here without affecting affecting files outside. To deactivate, type <code>deactivate</code>

- Rather than hunting around for the packages you need, you can install in one step. Type <code>pip install -r requirements.txt</code>. This will install all the packages listed in the respective file. If you install a package, make sure others know by updating the requirements.txt file. An easy way to do this is <code>pip freeze > requirements.txt</code>

- Flask requires that you set an environmental variable to the python file. However you do that, you'll want to set the file to be <code>server.py</code>. Check [here](https://flask.palletsprojects.com/en/1.1.x/quickstart/#a-minimal-application) for more details.   
    On UNIX:   
    <code>export FLASK_APP=server.py</code>   
    <code>export FLASK_ENV=development</code>  
    On Windows:  
    <code>$env:FLASK_APP = "server.py"</code>   
    <code>$env:FLASK_ENV = "development"</code>

- You should now be ready to test the application. In the directory, type either <code>flask run</code> or <code>python -m flask run</code>. The app should respond with an address you should be able to go to using your browser.

Current Setup:
----

The app is powered by [JSON files](https://www.tutorialspoint.com/json/json_quick_guide.htm). This is to get around having a DB until we actually need one. The main ones are:
     
* competitions.json - list of competitions
* clubs.json - list of clubs with relevant information. You can look here to see what email addresses the app will accept for login.

Testing: unit tests and integration tests
---

To run tests, in the directory type <code>pytest</code>.
when all tests are finished you can check coverage. A new directory htmlcov appeared. Open it and open index.html page in a web browser to see coverage report.

Testing: performance tests
---

To run performance tests you have to run app. In a terminal run flask app. App is running on [http://127.0.0.1:5000/](http://127.0.0.1:5000/)
    Open an other terminal and go in test_performance directory:  
    <code>cd tests</code>  
    <code>cd test_performance</code>  
    Then type <code>locust</code>
    
In the web browser open locust page: [http://localhost:8089/](http://localhost:8089/)
Choose number of user, spawn rate and indicate host app http://127.0.0.1:5000/. Then start swarming.

Documentation:
---

This project is part of [Openclassrooms](https://openclassrooms.com/fr/) training program Python Developer.

Courses:  
- [Débuggez un projet Python](https://openclassrooms.com/en/courses/7155851-debuggez-un-projet-python)

- [Testez votre projet Python](https://openclassrooms.com/en/courses/7155841-testez-votre-projet-python)

 Documentation:  
- [Flask](https://flask.palletsprojects.com/en/1.1.x/)
- [Pytest](https://he-arc.github.io/livre-python/pytest/index.html)
- [Locust](https://docs.locust.io/en/stable/index.html)
- [Selenium](https://selenium-python.readthedocs.io/index.html)
- [How to use fixtures](https://docs.pytest.org/en/latest/how-to/fixtures.html#how-to-fixtures)
- [Pytest mock plugin](https://pypi.org/project/pytest-mock/)

Others:
- [Test a Flask App with Selenium WebDriver - Part 1](https://scotch.io/tutorials/test-a-flask-app-with-selenium-webdriver-part-1)
- [PicklingError using live_server fixture on Windows #54](https://github.com/pytest-dev/pytest-flask/issues/54)
- [Pickling error on OS X / Python 3.8 (but not in 3.7) #104](https://github.com/pytest-dev/pytest-flask/issues/104)  

Remerciements:
---

Un énorme, gigantesque remerciement à ma mentor Sandrine Suire pour tout le temps passé et le soutien face aux difficultés, notament avec git.
Et un gros remerciement à la communauté du [Discord DA Python](http://discord.pythonclassmates.org/). 

