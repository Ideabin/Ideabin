Generic single-database configuration.

This [tutorial][1] will explain better than me but, for a quick list of commands you can have a look at this README or setup wiki. I hope before doing this you have created your virtualenv environment for this project by running

```
env/bin/pip3.x install -r requirements.txt
```
Now, to make the migrate environment run

```
$ cd Ideabin
$ env/bin/alembic init alembic
```
Following directories/files will get created in the project
Ideabin/
    alembic/
        env.py
        README
        script.py.mako
        versions/

Change the line ```sqlalchemy.url = driver://user:pass@localhost/dbname``` with

```sqlalchemy.url = mysql+mysqlconnector://user123:pass123@localhost/ideabin```

Now, run

```
$ env/bin/alembic revision -m "message"
```

This will create a template of migration script in the *alembic/versions/* directory having the 'any message' in the file name. You can change the *upgrade()* and *downgrade()* functions as given in this branch. For the first file the
```down_revision = None```
but for others following this migration script their *down_revision* will be equal to the version the file preceeding it, which in this case it the first file. After updating the script file run

```
$ env/bin/alembic upgrade head
```
This will update the database according to your migrations scripts. To downgrade the database you can do

```
$ env/bin/alembic downgrade base
```

All this was manual, I mean even for the basic updates you have to create the migration scripts. To autogenerate the basic things we have to make the autogeneration possible. For that replace,

```
# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = None
```
with

```
from myapp.mymodel import Base
target_metadata = Base.metadata
```

(Now, this above part I wasn't able to do. If you can then you're most welcome). Anyway, after doing that, run

```
$ env/bin/alembic revision --autogenerate -m "another message"
```
If it gives no errors then you are good to go. This above command will create a migration script in your versions directory doing the work you previously had to do manually. Now, this is just the creation of the migration script. To update the database run,

```
$ env/bin/alembic upgrade head
```
I was just able to follow the tutorial till here. For the capabilities of the autogeneration (what it can and can't do) and other advanced things, go have a look at the [tutorial][1].


[1]: http://alembic.readthedocs.org/en/latest/tutorial.html#the-migration-environment