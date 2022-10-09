import factory
import factory.django
from factory.fuzzy import FuzzyInteger, FuzzyDate
import datetime
from .models import Books, Author, Publisher, Student, Librarian
from django.contrib.auth.models import User
import random


year_choice = {
        '2012': '2012',
        '2013': '2013',
        '2014': '2014',
        '2015': '2015',
        '2016': '2016',
        '2017': '2017',
    }

class AuthorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Author
    
    firstname = factory.Faker('first_name')
    lastname = factory.Faker('last_name')
    dob = FuzzyDate(datetime.date(2000, 1, 1))
    fullname = factory.LazyAttribute(lambda p: '{} {}'.format(p.firstname, p.lastname))

class PublisherFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Publisher

    name = factory.Faker('company')
    city = factory.Faker('city')
    country = factory.Faker('country')

class BookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Books

    book_id = factory.Faker('pystr', max_chars=9)
    title = factory.Faker('bs')
    author = factory.SubFactory(AuthorFactory)
    isbn = FuzzyInteger(1000000000, 9999999999)
    publisher = factory.SubFactory(PublisherFactory)

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username',)
    
    username = factory.Faker('user_name')
    email = factory.Faker('email')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')

def get_semester():
    return random.randint(1,9)

def get_gender():
    gender_choices = [gender for gender in Student.GENDER_CHOICES]
    return random.choice(gender_choices)[0]

def get_branch():
    branch_choices = [branch for branch in Student.BRANCH_CHOICES]
    return random.choice(branch_choices)[0]

def get_enrollment():
    roll_pre = {
        'IIT': 'IIT',
        'IEC': 'IEC',
        'IWM': 'IWM',
        'ITM': 'ITM',
        'ICM': 'ICM',
        'ISM': 'ISM',
        'ISC': 'ISC',
    }
    yearval = random.choice(year_choice.keys())
    prefixval = random.choice(roll_pre.keys())
    number = str(random.randint(100,500))
    return prefixval + yearval + number

class StudentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Student
        django_get_or_create = ('user',)
        
    user = factory.SubFactory(UserFactory)
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    enrollment_no = factory.LazyFunction(get_enrollment)
    gender = factory.LazyFunction(get_gender)
    department = factory.LazyFunction(get_branch)
    semester = factory.LazyFunction(get_semester)
    fullname = factory.LazyAttribute(lambda k: '{} {}'.format(k.first_name, k.last_name))

def get_librarianid():
    number = str(random.randint(100,500))
    yearval = random.choice(year_choice.keys())
    return 'LIB' + yearval + number     

class LibrarianFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Librarian
        django_get_or_create = ('user',)
        
    user = factory.SubFactory(UserFactory)
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    librarian_id = factory.LazyFunction(get_librarianid)
    fullname = factory.LazyAttribute(lambda k: '{} {}'.format(k.first_name, k.last_name))