""" Data factory for creating instances of models in the application. """

from users.models import User
from organization.models import Branch
from services.models import Category, Service


def user_factory(username, email, password):
    return User(username=username, email=email, password=password)
def branch_factory(name, address="", phone_number="", email=""):
    return Branch(
        name=name,
        address=address,
        phone_number=phone_number,
        email=email
    )
def category_factory(name, description=""):
    return Category(name=name, description=description)
def service_factory(name, category, description=""):
    return Service(name=name, category=category, description=description)
