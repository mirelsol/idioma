This is a small application I wrote to improve my foreign language skills. Basically it randomly takes an expression in a given language and asks for its translation.
It uses the Django framework.
How it works
============
Administration
--------------
1. Run the app : ./manage.py runserver
2. Go to the Django Admin page (e.g. http://127.0.0.1:8000/admin)
3. Add the languages you want tot to manage. Click on "Add" next to "Languages"
4. Add the topics to classify the expressions.
5. Add the expressions.

Usage
-----
Just go to the start page (e.g. http://127.0.0.1:8000/idioma/).

Technical requirements
======================
* Django 1.7
* sqlite3
* Python 3
