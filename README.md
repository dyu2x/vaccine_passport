
# Vaccine Passport Project

## Table of Contents<a name="table"></a>
1. [Postgres database schema](#introduction)
2. Installation
    1. [Raw file](#setup)
    2. [ERD](#erd)
    3. [Database Installation](#database_setup)
    4. File Setup
        1. models.py
            - [Account Class](#account_class)
            - [Provider Class](#provider_class)
            - [Facility Class](#facility_class)
            - [Passport Class](#passport_class)
            - [Facility-Providers](#facility_provider)
        2.  API Files
            - [Accounts](#accounts.py)
            - [Facilities](#facilities.py)
            - [Passports](#passports.py)
            - [Providers](#providers.py)
        3.  [init File](#__init__.py)
    5. Insomnia setup
        1. [Download Application](#download_application)
        2. [Import json file](#Import_json_file)
        3. Operations:
            - [Providers](#providers)
            - [Facilities](#facilities)
            - [Accounts](#accounts)
            - [Passports](#passports)
    6. [Start Virtual Environtment](#startv)
    7. [Start Server](#start)
3. Other Documentation
    1. [Reset Primary Key](#reset)
    2. [Load faker data](#faker)
3. [Contributing](#contributing)
4. [License](#license)
5. [Credits](#credit)

### Postgres database schema <a name="introduction"></a>[&#8593;](#table)

The Vaccine Passport database has 1 fact table which is the Passports, and 3 dimensional tables which are accounts, 
facilities, and providers.

![Alt text](https://www.dropbox.com/s/b5dlyo1nykr1029/Vaccine_Passport_db_schema.png?raw=true "db Schema")

## Installation

### Setup: <a name="setup"></a>[&#8593;](#table)

We have included the raw files for this project (project_raw.zip)
- unzip this file on your computer.
- make sure that your virtual environment is running

### ERD: <a name="erd"></a>[&#8593;](#table)

![Alt text](https://www.dropbox.com/s/736jnw1v1utt1z0/vaccine_passport.png?raw=true "ERD") 

### Database Setup<a name="database_setup"></a>: [&#8593;](#table)

+ Database creation:
	- Create a database name “vaccine_passport” on pgadmin or you can run this command on 
	
        ```bash
        % docker exec -i pg_container psql -c 'CREATE DATABASE vaccine_passport;’
        ```
	- please check your server if the server has been created or if you did it using the terminal, the 	terminal should return 

            CREATE DATABASE


+ loading Tables and records.
	- You can load the program database step by step with the option to modify the tables properly in the future. these steps will create a migrations version.

### File Setup

models.py

#### Create Account Class<a name="account_class"></a> [&#8593;](#table)

```python
from flask_sqlalchemy import SQLAlchemy
import datetime
db = SQLAlchemy()
 
 
class Account(db.Model):
   __tablename__ = 'accounts'
   id = db.Column(db.Integer, primary_key=True, autoincrement=True)
   first_name = db.Column(db.String(128), nullable=False)
   last_name = db.Column(db.String(128), nullable=False)
   username = db.Column(db.String(128), unique=True, nullable=False)
   password = db.Column(db.String(128), nullable=False)
   address = db.Column(db.String(128), nullable=False)
   birthdate = db.Column(db.DateTime, default=datetime, nullable=False)
 
   def __init__(self, first_name: str, last_name: str, username: str, password: str, address: str, birthdate: int):
       self.first_name = first_name
       self.last_name = last_name
       self.username = username
       self.password = password
       self.address = address
       self.birthdate = birthdate
 
   def serialize(self):
       return {
           'id': self.id,
           "first_name": self.first_name,
           "last_name": self.last_name,
           'username': self.username,
           "address": self.address,
           "birthdate": self.birthdate
       }

```

> And you should be within the vaccine_passport folder

on Terminal

```bash 
% cd vaccine_passport
```
```bash 
% flask db migrate
```

> This will create a new file found migrations/versions


```bash 
% flask db upgrade
```

>This will create an Accounts table on the vaccine_provider database

on models.py

#### Create Provider Class<a name="provider_class"></a> [&#8593;](#table)
type this code right after the accounts class.
exclude (...)

```python
...

class Provider(db.Model):
   __tablename__ = 'providers'
   id = db.Column(db.Integer, primary_key=True, autoincrement=True)
   name = db.Column(db.String(128), unique=True, nullable=False)
 
   def __init__(self, name: str):
       self.name = name
 
   def serialize(self):
       return {
           'id': self.id,
           'name': self.name,
       }

```

on Terminal

```bash 
% flask db migrate
```

> This will create a new file found migrations/versions

```bash 
% flask db upgrade
```

> This will create a Providers table on the vaccine_provider database

```bash 
% flask db migrate
```

on models.py
#### Create Facility Class<a name="facility_class"></a> [&#8593;](#table)

type this code right after the providers class.
exclude (...)

```python
...

class Facility(db.Model):
   __tablename__ = 'facilities'
   id = db.Column(db.Integer, primary_key=True, autoincrement=True)
   name = db.Column(db.String(128), unique=True, nullable=False)
   address = db.Column(db.String(128), nullable=False)
   code = db.Column(db.String(128), unique=True, nullable=False)
 
   def __init__(self, name: str,  address: str, code: str):
       self.name = name
       self.address = address
       self.code = code
 
   def serialize(self):
       return {
           'id': self.id,
           'name': self.name,
           'address': self.address,
           "code": self.code
       }

```

on Terminal

```bash 
% flask db migrate
```

> This will create a new file found migrations/versions


```bash 
% flask db upgrade
```

> This will create a Facility table on the vaccine_provider database.

On models.py
#### Create Passport Class<a name="passport_class"></a> [&#8593;](#table)

type this code right after the Facility class.
exclude (...)

```python
...

class Passport(db.Model):
   __tablename__ = 'passports'
   id = db.Column(db.Integer, primary_key=True, autoincrement=True)
   date_administered1 = db.Column(
       db.Date,
       default=datetime.datetime.utcnow,
       nullable=False
   )
   date_administered2 = db.Column(
       db.Date
   )
   date_administered3 = db.Column(
       db.Date
   )
   provider_id1 = db.Column(db.Integer, db.ForeignKey(
       'providers.id'))
   provider_id2 = db.Column(db.Integer, db.ForeignKey(
       'providers.id'), nullable=True)
   provider_id3 = db.Column(db.Integer, db.ForeignKey(
       'providers.id'), nullable=True)
   account_id = db.Column(db.Integer, db.ForeignKey(
       'accounts.id'), nullable=False)
   facility_id1 = db.Column(db.Integer, db.ForeignKey(
       'facilities.id'))
   facility_id2 = db.Column(db.Integer, db.ForeignKey(
       'facilities.id'), nullable=True)
   facility_id3 = db.Column(db.Integer, db.ForeignKey(
       'facilities.id'), nullable=True)
 
    # uncomment __init__ before using seed.py and comment after use
    # def __init__(self, provider_id1: int, date_administered1: int, date_administered2: int, date_administered3: int, provider_id2: int, provider_id3: int, account_id: int, facility_id1: int, facility_id2: int, facility_id3: int):

    #     self.account_id = account_id
    #     self.provider_id1 = provider_id1
    #     self.facility_id1 = facility_id1
    #     self.provider_id2 = provider_id2
    #     self.facility_id2 = facility_id2
    #     self.provider_id3 = provider_id3
    #     self.facility_id3 = facility_id3
    #     self.date_administered1 = date_administered1 
    #     self.date_administered2 = date_administered2
    #     self.date_administered3 = date_administered3

    # place comment on me if the first __init___ func is in use
    def __init__(self, provider_id1: int, provider_id2: int, provider_id3: int, account_id: int, facility_id1: int, facility_id2: int, facility_id3: int): 
        self.account_id = account_id
        self.provider_id1 = provider_id1
        self.facility_id1 = facility_id1
        self.provider_id2 = provider_id2
        self.facility_id2 = facility_id2
        self.provider_id3 = provider_id3
        self.facility_id3 = facility_id3
 
   def serialize(self):
       return {
           'account_id': self.account_id,
           'provider_id1': self.provider_id1,
           'facility_id1': self.facility_id1,
           'date_administered1': self.date_administered1,
           'provider_id2': self.provider_id2,
           'facility_id2': self.facility_id2,
           'date_administered2': self.date_administered2,
           'provider_id3': self.provider_id3,
           'facility_id3': self.facility_id3,
           'date_administered3': self.date_administered3,
        }

```

on Terminal

```bash 
% flask db migrate
```

> This will create a new file found migrations/versions

```bash 
% flask db upgrade
```

> This will create a Passports table on the vaccine_provider database.

on models.py

Then insert facility_providers code in between Facility and Provider class.

#### facility providers<a name="facility_provider"></a> [&#8593;](#table)
exclude (...)

```python
...

facility_provider_table = db.Table(
   'facility_provider',
   db.Column(
       'provider_id', db.Integer,
       db.ForeignKey('providers.id'),
       primary_key=True
   ),
 
   db.Column(
       'facility_id', db.Integer,
       db.ForeignKey('facilities.id'),
       primary_key=True
   )
)

...
```

on Terminal

```bash 
% flask db migrate
```
> This will create a new file found migrations/versions


```bash 
% flask db upgrade
```

> This will create a facility_providers table on the vaccine_provider database

on models.py

Insert this code before the def __init__  on your class Facility.
exclude (...)

```python
...

   facility_providers = db.relationship(
       'Provider', secondary=facility_providers_table,
       lazy='subquery',
       backref=db.backref('facility_providers_list', lazy=True))
 
...
```

on Terminal

```bash 
% flask db migrate
```
> no new migration file will be created at this time

```bash 
% flask db upgrade
```

> We are now done with the database setup, we can now complete other files needed for this project.

- you can start from no data. you can use the data.sql to load some made up data to populate the database. check the "raw sql" folder 

Files setup:
- We need to create an api folder within our project

on Terminal

```bash 
% mkdir src/api
```
```bash 
% cd src/api
```

> we now need to create 4 py files

```bash 
touch accounts.py providers.py facilities.py passports.py
```
open API folder

#### accounts.py<a name="accounts.py"></a> [&#8593;](#table)
> we should have this code on this file

```python
from flask import Blueprint, jsonify, request
from ..models import Account, Passport, Facility, Provider, db
import hashlib
import datetime
import secrets


def scramble(password: str):
    """Hash and salt the given password"""
    salt = secrets.token_hex(16)
    return hashlib.sha512((password + salt).encode('utf-8')).hexdigest()


bp = Blueprint('accounts', __name__, url_prefix='/accounts')


@bp.route('', methods=['GET'])  # qorking
def index():
    accounts = Account.query.all()  # ORM perjsons SELECT query
    result = []
    for t in accounts:
        result.append(t.serialize())
    return jsonify(result)  # return JSON response


@ bp.route('', methods=['POST'])  # working
def create():

    a = Account(
        first_name=request.json['first_name'],
        last_name=request.json['last_name'],
        username=request.json['username'],
        password=scramble(request.json['password']),
        address=request.json['address'],
        birthdate=request.json['birthdate']
    )

    if request.json['password'] != request.json['Verify Password']:
        return jsonify('Password should match!')
    if len(request.json['password']) < 8:
        return jsonify('Password should be greater than 8 characters')
    if len(request.json['username']) < 4:
        return jsonify('Username should be greater than 4 characters')
    try:
        db.session.add(a)
        db.session.commit()
        account_name = request.json['username']
        usrname = Account.query.filter_by(username=account_name).first()
        provider_name = request.json['provider']
        prov = Provider.query.filter_by(name=provider_name).first()
        facility_code = request.json['facility']
        fclty = Facility.query.filter_by(code=facility_code).first()
        p = Passport(
            provider_id1=prov.id,
            account_id=usrname.id,
            facility_id1=fclty.id,
            provider_id2=prov.id,
            facility_id2=fclty.id,
            provider_id3=prov.id,
            facility_id3=fclty.id

        )
        db.session.add(p)
        db.session.commit()
        return jsonify('Registration Successful!')
    except:
        return jsonify('Username Unavailable!')


@bp.route('/search', methods=['GET'])  # working
def search():
    username = request.json['username']
    acnt = Account.query.filter_by(username=username).first()

    try:
        return jsonify(acnt.serialize())
    except:
        return jsonify('Username not found!')


@bp.route('/<int:id>', methods=['PATCH'])  # working
def update(id: int):
    account_id_info = Account.query.get_or_404(id)
    if 'address' in request.json:
        account_id_info.address = request.json['address'],
    if 'username' in request.json:
        account_id_info.username = request.json['username']
    if 'password' in request.json:
        account_id_info.password = scramble(request.json['password'])
    try:
        db.session.commit()
        return jsonify('Profile updated!')
    except:
        return jsonify(False)

```

save

#### facilities.py<a name="facilities.py"></a> [&#8593;](#table)

> we should have this code on this file

```python
from flask import Blueprint, jsonify, request
from ..models import Facility, Account, Passport, Provider, db
import datetime

bp = Blueprint('facilities', __name__, url_prefix='/facilities')


@bp.route('', methods=['GET'])  # working
def index():
    facilities = Facility.query.all()  # ORM perjsons SELECT query
    result = []
    for t in facilities:
        result.append(t.serialize())
    return jsonify(result)  # return JSON response


@bp.route('/<int:id>', methods=['GET'])  # working
def show(id: int):
    t = Facility.query.get_or_404(id)
    return jsonify(t.serialize())


@bp.route('', methods=['POST'])  # working
def open_new_facility():
    fn = request.json['Facility name']
    fa = request.json['address']
    fc = request.json['code']
    f = Facility(
        name=fn,
        address=fa,
        code=fc
    )
    if len(request.json['Facility name']) < 4:
        return jsonify('Enter Valid Name')
    if len(request.json['address']) < 5:
        return jsonify('Enter Valid Address')

    try:
        db.session.add(f)
        db.session.commit()  # execute CREATE statement
        return jsonify('Registration Successful!')
    except:
        return jsonify('Name Unavailable!')


@bp.route('/search', methods=['GET'])  # working
def search():
    code = request.json['code']
    acnt = Facility.query.filter_by(code=code).first()

    try:
        # account_id_info = Account.query.get(acnt.id)
        return jsonify(acnt.serialize())
    except:
        return jsonify('Username not found!')


@bp.route('/vax', methods=['PATCH'])  # not working
def administer():

    account_name = request.json['username']
    usrname = Account.query.filter_by(username=account_name).first()
    accountid_info = Passport.query.filter_by(account_id=usrname.id).first()
    provider_name = request.json['provider']
    prov = Provider.query.filter_by(name=provider_name).first()
    facility_code = request.json['facility']
    fclty = Facility.query.filter_by(code=facility_code).first()
    if accountid_info.date_administered2 == None:
        accountid_info.date_administered2 = request.json['Administered date']
        accountid_info.provider_id2 = prov.id
        accountid_info.facility_id2 = fclty.id
        db.session.commit()
        return jsonify('Second dose administered!')
    if accountid_info.date_administered3 == None:
        accountid_info.date_administered3 = request.json['Administered date']
        accountid_info.provider_id3 = prov.id
        accountid_info.facility_id3 = fclty.id
        db.session.commit()
        return jsonify('Third dose administered!')
    return jsonify('Vaccines are up to date')

```

save

#### passports.py<a name="passports.py"></a> [&#8593;](#table)
> we should have this code on this file

```python
from datetime import date
from flask import Blueprint, jsonify, request
from ..models import Account, Passport
from sqlalchemy import func
func.avg(...)
func.sum(...)
func.max(...)

bp = Blueprint('passports', __name__, url_prefix='/passports')


@bp.route('/<int:id>', methods=['GET'])  # working
def show(id: int):
    t = Passport.query.get_or_404(id)
    return jsonify(t.serialize())

@bp.route('', methods=['GET'])  # decorator takes path and list of HTTP verbs
def index():
    accounts = Passport.query.all()  # ORM perjsons SELECT query
    result = []
    for t in accounts:
        result.append(t.serialize())
    return jsonify(result)  # re

@bp.route('/search', methods=['POST'])  # working
def search():
    account_name = request.json['username']
    passp = Account.query.filter_by(username=account_name).first()
    new = Passport.query.filter_by(account_id=passp.id).first()
    return jsonify(new.serialize())

@bp.route('/search', methods=['POST'])  # working
def test():
    account_name = request.json['username']
    usrname = Account.query.filter_by(username=account_name).first()
    passp = Passport.query.max(usrname.id)
    max_dose = max(passp.dose)
    return jsonify(max_dose)
```

save

#### providers.py<a name="providers.py"></a> [&#8593;](#table)
> we should have this code on this file

```python
from flask import Blueprint, jsonify, request
from ..models import Provider, db

bp = Blueprint('providers', __name__, url_prefix='/providers')


@bp.route('', methods=['GET'])  # working
def index():
    providers = Provider.query.all()  # ORM performs SELECT query
    result = []
    for t in providers:
        result.append(t.serialize())
    return jsonify(result)  # return JSON response

@bp.route('/<int:id>', methods=['GET'])  # working
def show(id: int):
    t = Provider.query.get_or_404(id)
    return jsonify(t.serialize())

@bp.route('', methods=['POST'])  # working
def create_new_provider():
    pn = request.json['Provider name']
    p = Provider(
        name=pn
    )
    if len(request.json['Provider name']) < 4:
        return jsonify('Enter Valid Name')

    try:
        db.session.add(p)
        db.session.commit()  # execute CREATE statement
        return jsonify('Registration Successful!')
    except:
        return jsonify('Name Unavailable!')

```

save

On src folder 
#### __init__.py<a name="__init__.py"></a> [&#8593;](#table)
uncomment lines 34 to 38
```python
   from .api import facilities, providers, passports, accounts
   app.register_blueprint(accounts.bp)
   app.register_blueprint(facilities.bp)
   app.register_blueprint(providers.bp)
   app.register_blueprint(passports.bp)
```

save

### Insomnia setup

#### Download Application<a name="download_application"></a>: [&#8593;](#table)

You can download Insomnia [here](https://insomnia.rest/download). Installation instructions [here](https://docs.insomnia.rest/insomnia/install/)

#### Import json file<a name="Import_json_file"></a>: [&#8593;](#table)

- Open Insomnia program
- on the top left, click on "Insomnia" 
- on the upper right of the program, click on "create" then "File" 
- search for the Insomnia_2022-01-31.json located on the REST API folder
- once successful, it should return an "Import Succeded" window
- Now, you should have a collection named "Passport API"

#### - Operations:

##### <ins>PROVIDERS</ins> <a name="providers"></a>: [&#8593;](#table)

- index

> this will show the list of providers available on your database

- create_new_provider

> this will create new provider 

```bash 
{
	"Provider name": ""
}
```

- show

> this will show the information of the a provider by using the provider id on our index.

##### <ins>FACILTIES</ins> <a name="facilities"></a>: [&#8593;](#table)

- open_new_facility

> this will create a new facility on our database.

```bash 
{
	"Facility name": "Mesina III Heart Center",
	"address": "123 1st st, Sunnyvale",
	"code":"MHC-009"
}
```

- administer

> this will create second and third administer record for a patient/user.

```bash 
{
	"username": "test2",
	"provider": "Moderna",
	"facility": "MHC-009",
	"Administered date": "2021-02-01"
}
```
- search

> you can search for information of a facility using the facility code

```bash 
{
	"code": "GVH-272"
}
```

##### <ins>ACCOUNTS</ins> <a name="accounts"></a>: [&#8593;](#table)

- index

> this will show the list of accounts available on your database

```bash 
[
	{
		"address": "12a3 4th st Mountain View",
		"birthdate": "Sat, 01 Jan 2000 00:00:00 GMT",
		"first_name": "TEST1",
		"id": 1,
		"last_name": "testqweqweqwe",
		"username": "test2"
	},
	{
		"address": "12a3 4th st Mountain View",
		"birthdate": "Sat, 01 Jan 2000 00:00:00 GMT",
		"first_name": "TEST1",
		"id": 2,
		"last_name": "testqweqweqwe",
		"username": "test3"
	},
	{
		"address": "12a3 4th st Mountain View",
		"birthdate": "Sat, 01 Jan 2000 00:00:00 GMT",
		"first_name": "TEST1",
		"id": 3,
		"last_name": "testqweqweqwe",
		"username": "test"
	}
```

- search

> use username to search an account information 

```bash 
{
	"username": "test"
}
```

> result:

```bash 
{
	"address": "12a3 4th st Mountain View",
	"birthdate": "Sat, 01 Jan 2000 00:00:00 GMT",
	"first_name": "TEST1",
	"id": 1,
	"last_name": "testqweqweqwe",
	"username": "test"
}
```

- create 

> This is the account creation page, it will require you to complete all information needed. and at the same time, it will create your first administered shots which can be found at the passports table on your database.

```bash 
{
	"first_name": "TEST1",
	"last_name": "testqweqweqwe",
	"username": "zxczcx",
	"password": "pasword1234",
	"Verify Password": "pasword1234",
	"address": "12a3 4th st Mountain View",
	"birthdate": "2000-01-01",
	"provider": "Moderna",
	"facility": "RGCH-237"
}
```

> the result would be if all data are provided

```bash 
"Registration Successful!"
```

- update

> use the account_id of the user that requires an update

```bash 
{
	"password": "123412313"
}
```

> this would be the result if an update is successful

```bash 
"Profile updated!"
```

##### <ins>PASSPORTS</ins> <a name="passports"></a>: [&#8593;](#table)

- index

> this will show you all administered shot list on our database

> result:

```bash 
[
	{
		"account_id": 1,
		"date_administered": "Sun, 30 Jan 2022 00:00:00 GMT",
		"dose": 1,
		"facility_id": 1,
		"provider_id": 3
	},
	{
		"account_id": 2,
		"date_administered": "Sun, 30 Jan 2022 00:00:00 GMT",
		"dose": 1,
		"facility_id": 1,
		"provider_id": 3
	}
```

- search

> use username to search for an individual administered record

```bash 
{
	"username": "m_owen"
}
```

> result:

```bash 
{
	"account_id": 7,
	"date_administered": "Mon, 17 Feb 2020 00:00:00 GMT",
	"dose": 1,
	"facility_id": 12,
	"provider_id": 1
}

```

### Start Virtual Environment <a name="startv"></a>: [&#8593;](#table)

> make sure that you are on the same path where the vend folder is located prior running the command

on Terminal

```bash 
 . ../venv/bin/activate
```
> you should see "(venv)" before the name of your computer on the terminal

### Start Server <a name="start"></a>: [&#8593;](#table)
> we are now ready to run the server. prior running this command, make sure that you are within the vaccine_passport path. if not, type

on Terminal

```bash 
% cd vaccine_passport
```

> if you are already within the vaccine_passport path, type these commands

on Terminal

```bash 
% export FLASK_ENV=development
```
```bash 
% flask run
```

> You should have a similar result

![Alt text](https://www.dropbox.com/s/077le1lv0h2tcp7/flask.png?raw=true "flask")



## Other documentations

### Reset Primary Key to 1 <a name="reset"></a> [&#8593;](#table)

After deleting all data (Passport and Accounts) you can reset the Primary Key to 1
on your Query tool, type

```bash 
ALTER SEQUENCE passports_id_seq RESTART WITH 1
```

> to reset passport primary key

```bash 
ALTER SEQUENCE accounts_id_seq RESTART WITH 1
```

> to reset accounts primary key

### Load faker data (Accounts and Passport table)<a name="faker"></a> [&#8593;](#table)
Must be on the same directory where your seed.py is located

```bash 
% python3 seed.py
```
adter loading the files, Accounts and Passports table are now populated with fake data


## Contributing <a name="contributing"></a>: [&#8593;](#table)
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
Please make sure to update tests as appropriate. email me, I guess

## License <a name="license"></a>: [&#8593;](#table)
none at this time

## Credits <a name="credit"></a>: [&#8593;](#table)
Thank you NuCamp for the lessons to create my first program and to Miss Selena Flannery -- Instructor for guidance. The files that created is program is based on the Twitter assignment that we use.
