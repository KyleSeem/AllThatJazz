from __future__ import unicode_literals

from django.db import models
from datetime import datetime, date
import bcrypt

# Create your models here.
class UserManager(models.Manager):
    def login(self, postData):
        username = postData['username']
        password = postData['password']

        alerts = []

        if len(username) < 1:
            alerts.append('Please enter username.')
        try:
            user = User.objects.get(username=username)
        except:
            print ('USERNAME NOT REGISTERED')
            alerts.append('The username "{}" is either incorrect or has not been registered.'.format(username))
            return (False, alerts)
        else:
            if username == user.username:
                if bcrypt.hashpw(password.encode(), user.pw_hashed.encode()) == user.pw_hashed:
                    # print ('it matches', user.id)
                    return (True, 'back, {}!'.format(user.username), user.id)
                else:
                    # print ('no pw match')
                    alerts.append('The password entered is incorrect. Please try again.')

            if alerts:
                return (False, alerts)


    def register(self, postData):
        # grabs user input from registration form
        name = str(postData['name'])
        username = str(postData['username'])
        hire_date = postData['hire_date']
        password = postData['password']
        pw_verify = postData['pw_verify']

        alerts = []

        if len(name) < 1:
            alerts.append('Name cannot be left blank.')

        if len(username) < 3:
            alerts.append('Username must be at least 3 characters in length.')

        if len(postData['hire_date']) < 1:
            alerts.append('Hire date cannot be left blank.')
        else:
            hire_date = datetime.strptime(postData['hire_date'], '%Y-%m-%d')
            if hire_date > datetime.today():
                print ('HIRE DATE IN FUTURE')
                alerts.append('Hire date cannot be in the future.')

        if len(password) < 8:
            alerts.append('Password must be at least 8 characters in length.')
        elif password != pw_verify:
            alerts.append('Passwords do not match.')

        if alerts:
            return (False, alerts)
        # else:
        #     try:
        #         User.objects.get(name=name)
        #     except:
        #         print ('USER ALREADY EXISTS')
        #         alerts.append('The name "{}" has already been registered.'.format(name))
        #         return (False, alerts)
        else:
            pw_hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            user = User.objects.create(name=name, username=username, hire_date=postData['hire_date'], pw_hashed=pw_hashed)
            return (True, 'aboard, {}!'.format(username), user.id)


class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    hire_date = models.DateField(auto_now=False)
    pw_hashed = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    userManager = UserManager()
    objects = models.Manager()
