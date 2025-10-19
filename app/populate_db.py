from faker import Faker
from app.routers.utils import db_users

faker = Faker("pt_BR")

for _ in range (1000):
    register = {
        "name": faker.name(),
        "email": faker.email(),
        "passwd": faker.password(),
        "register_date": faker.date_time(),
        "active": 'True'
    }
    db_users.insert(register)
