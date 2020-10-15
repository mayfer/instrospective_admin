# Introspective Django Admin Panel

This is a re-usable Django Admin Panel. It auto-generates all models on-the-fly from your existing database tables.

All you need for configuration is database settings.

0. `pip install -r requirements.txt`
1. `cp credentials.py.example credentials.py` and fill in your credentials.
2. Run `python run.py migrate`, this will create additional tables for the admin panel (note: they will be prefixed `auth_` and `django_` so they shouldn't really clash with your database)
3. Run `python run.py createsuperuser` for the admin login
4. Run `python run.py` (or alternatively `python run.py runserver 0.0.0.0:8000`)

Voila, you should now be able to view your entire database in a Django Admin Panel.

After that, you can customize the admin panel via normal methods by editing `admin_panel.py`.