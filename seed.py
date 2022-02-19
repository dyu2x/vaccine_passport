"""
Populate twitter database with fake data using the SQLAlchemy ORM.
"""

from ctypes import addressof
import random
import string
import hashlib
import secrets
from faker import Faker
from vaccine_passport.src.models import Account, Facility, Passport, Provider, db
from vaccine_passport.src import create_app
from faker.providers import BaseProvider

ACCOUNT_COUNT = 600
PASSPORT_COUNT = 600
FACILITY_COUNT = 20
PROVIDER_COUNT = 5

# assert LIKE_COUNT <= (USER_COUNT * TWEET_COUNT)


def random_passhash():
    """Get hashed and salted password of length N | 8 <= N <= 15"""
    raw = ''.join(
        random.choices(
            string.ascii_letters + string.digits + '!@#$%&',  # valid pw characters
            k=random.randint(8, 15)  # length of pw
        )
    )

    salt = secrets.token_hex(16)

    return hashlib.sha512((raw + salt).encode('utf-8')).hexdigest()


def truncate_tables():
    #     """Delete all rows from database tables"""
    #     db.session.execute(likes_table.delete())
    Passport.query.delete()
    Account.query.delete()
    db.session.commit()


def main():
    """Main driver function"""
    app = create_app()
    app.app_context().push()
    truncate_tables()
    fake = Faker()

    last_user = None  # save last user
    for _ in range(ACCOUNT_COUNT):
        last_user = Account(
            username=fake.unique.first_name().lower() + str(random.randint(1, 150)),
            password=random_passhash(),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            address=fake.address(),
            birthdate=fake.date_of_birth(minimum_age=12, maximum_age=80)
        )
        db.session.add(last_user)

    # insert users
    db.session.commit()

    passp = None  # save last user
    for _ in range(PASSPORT_COUNT):
        passp = Passport(
            date_administered1=fake.date_between(
                start_date='-3y', end_date='-3m'),
            date_administered2=None,
            date_administered3=None,
            provider_id1=random.randint(1, 4),
            facility_id1=random.randint(1, 20),
            provider_id2=random.randint(1, 4),
            facility_id2=random.randint(1, 20),
            provider_id3=random.randint(1, 4),
            facility_id3=random.randint(1, 20),
            account_id=random.randint(
                last_user.id - ACCOUNT_COUNT + 1, last_user.id)
        )
        db.session.add(passp)

    # insert users
    db.session.commit()


main()
