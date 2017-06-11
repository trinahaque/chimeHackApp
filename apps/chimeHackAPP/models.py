from __future__ import unicode_literals
from django.db import models
import re, bcrypt
from datetime import datetime, date
NAME_REGEX = re.compile(r'/^[a-zA-Z]+', re.MULTILINE)
PASSWORD_REGEX = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*(_|[^\w])).+$', re.MULTILINE)

class UserManager(models.Manager):

    def registration(self, POST):
        first_name = POST['first_name'].lower()
        last_name = POST['last_name'].lower()
        username = POST['username'].lower()
        password = POST['password']
        skill_level = POST['skill_level']
        language = POST['language'].lower()
        location = POST['location'].lower()

        errors = []

        valid = True
        if len(first_name) < 1 or len(last_name) < 1 or len(username) < 1 or len(password) < 1 or len(skill_level) < 1 or len(language) < 1 or len(location) < 1:
            errors.append("A field can not be empty")
            valid = False
        else:
            # names
            # password
            if len(password) < 6:
                errors.append("Password needs at least 6 characters")
                valid = False

        if valid:
            distinct_list = User.objects.filter(username = username)
            if not distinct_list:
                pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
                language = Language.objects.create(language=language)
                user = User.objects.create(first_name=first_name, last_name=last_name, language=language, location=location, username=username, password=pw_hash, skill_level=skill_level)
                return (True, user)
            else:
                # valid_messages.append("Email already exists")
                errors.append("User already exists")

        return (False, errors)


    def login(self, POST):

        username = POST['username'].lower()
        password = POST['password']

        login_messages = []

        if len(username) < 1 or len(password) < 1:
            login_messages.append("A field can not be empty")

        if len(password) < 8:
            login_messages.append("Password needs at least 8 characters")

        if len(login_messages) < 1:
            user = User.objects.filter(username=username)
            # print user
            if len(user) > 0:
                if bcrypt.hashpw(password.encode(), user[0].password.encode()) == user[0].password.encode():
                    return True, user[0]
                else:
                    login_messages.append("Wrong password")
            else:
                login_messages.append("Not a registered user")
        return False, login_messages


class EssayManager(models.Manager):
    def validateEssay(self, POST, id):
        title = POST['title']
        essay = POST['essay']

        errors = []
        if len(title) < 1 or len(essay) < 1:
            errors.append("A field can not be empty")
        else:
            user = User.objects.get(id=id)
            essay = Essay.objects.create(user=user, title=title, essay=essay)
            return True, essay

        return False, errors


class Language(models.Model):
    language = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now=True)


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=200)
    skill_level = models.IntegerField()
    language = models.ForeignKey(Language)
    location = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


class Essay(models.Model):
    title = models.CharField(max_length=255)
    essay = models.TextField()
    user = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = EssayManager()
