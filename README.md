Quiz Forward
===
This is the engine of the quiz forward project. It allows the extraction of
articles from various sources to various destinations (on screen display, on disk, database).

# Required modules
The number between the parenthesis represents the version used during the
development phase. Other versions might as well work.

* Peewee (2.2.2)
* PyMySQL3 (0.5)
* Yaspy (1.10.223)

# Plugins instructions

## Database

A file named `kbextractor/plugins/destinations/database/settings.py` and containing the information to connect to the database is required by this plugin.
The file must look like this:


    import peewee

    db = peewee.MySQLDatabase("my_database",
                              user="my_user",
                              password="my_password")


The `populate.py` script will help you to create your database and the tables.

# Usage examples

`python3 main.py --source PyDesk --source-options subdomain=my_domain,username=my_username@my_domain.com,password=my_password --destination=OSD`