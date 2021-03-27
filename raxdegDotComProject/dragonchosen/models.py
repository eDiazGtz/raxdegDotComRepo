from django.db import models
from django.shortcuts import redirect
from django.contrib import messages
import re, bcrypt

# Create your models here.


class UserManager(models.Manager):
    def registrationValidator(self, postData):
        errors = {}
        if len(postData['firstName']) < 2:
            errors["firstName"] = "First Name must be longer than 1 character."
        if len(postData['lastName']) < 2:
            errors["lastName"] = "Last Name must be longer than 1 character."
        if len(postData['username']) < 1:
            errors["username"] = "Username Required."
        uniqueUsername = User.objects.filter(username=postData['username'])
        if len(uniqueUsername) >= 1:
            errors['duplicateUsername'] = "Username Taken."
        # EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') #RegEx variable. alphanumeric ". and _ and - and +" + @ + alphanumeric ". and _ and - " + . + alpha
        # if not EMAIL_REGEX.match(postData['email']):
        #     errors['email'] = "Invalid email address."        
        if len(postData['password']) < 8:
            errors["password"] = "Password must at least 8 characters."
        if postData['password'] != postData['passwordConfirm']:
            errors["passwordConfirm"] = "Passwords do not match."
        return errors

    def loginValidator(self, postData):
        errors = {}
        user = User.objects.filter(username=postData['username'])
        if not len(user) > 0:
            errors["badCredentials"] = "Bad Credentials"
            return errors
        user = user[0]
        if bcrypt.checkpw(postData['password'].encode(), user.password.encode()) == False:
            errors["badCredentials"] = "Bad Credentials"
        return errors

    def passwordValidator(self, postData, user):
        errors = {}
        print(user.firstName)
        if bcrypt.checkpw(postData['password'].encode(), user.password.encode()) == False:
            errors["password"] = "Invalid Credentials."
        if len(postData['passwordNew']) < 8:
            errors["passwordNew"] = "New Password must at least 8 characters."
        if postData['passwordNew'] != postData['passwordConfirm']:
            errors["passwordConfirm"] = "New Passwords do not match."
        return errors

    def updateValidator(self, postData, usernamePresent):
        errors = {}
        if len(postData['firstName']) < 2:
            errors["firstName"] = "First Name must be longer than 1 character."
        if len(postData['lastName']) < 2:
            errors["lastName"] = "Last Name must be longer than 1 character."
        if len(postData['username']) < 2:
            errors["username"] = "Last Name must be longer than 1 character."
        uniqueUsername = User.objects.filter(username=postData['username'])
        if postData['username'] != usernamePresent:
            if len(uniqueUsername) >= 1:
                errors['duplicateUsername'] = "Username Taken."
        return errors

    def isLoggedIn(self, sessionData):
        errors = {}
        if('userId' not in sessionData):
            errors["noLogin"] = "Oops! Login Required to be here! Please log in or Register."
        return errors
    
    def errorsPresent(self, errors, request):
        if(len(errors) > 0):
            for key, value in errors.items():
                messages.error(request, value)
                return True
        return False


class CharacterManager(models.Manager):
    def registrationValidator(self, postData):
        errors = {}
        if len(postData['name']) < 1:
            errors["name"] = "Name is required."
        if postData['level'] < 1 or postData['level'] > 20:
            errors['level'] = "Invalid Level, must be between 1 and 20."
        if postData['ac'] < 10:
            errors["ac"] = "AC too low, please review AC calculation.\n(Unarmored: 10 + your Dexterity modifier. \nArmored: Use the AC entry for the armor you’re wearing (see PH, 145). \nFor example, in leather armor, you calculate your AC as 11 + your Dexterity modifier, and in chain mail, your AC is simply 16. \nUnarmored Defense (Barbarian): 10 + your Dexterity modifier + your Constitution modifier. \nUnarmored Defense (Monk): 10 + your Dexterity modifier + your Wisdom modifier. \nDraconic Resilience (Sorcerer): 13 + your Dexterity modifier. \nNatural Armor: 10 + your Dexterity modifier + your natural armor bonus. \nThis is a calculation method typically used only by monsters and NPCs, although it is also relevant to a druid or another character who assumes a form that has natural armor.)"
        if postData['ac'] > 25:
            errors["ac"] = "AC too high... contratry to personal belief, you are NOT a God."
        # # IF API USED
            # allClasses = ""
            # for class in allClassesAPI:
            #     allClasses += class
            # if postData['class'] not in allClasses:
            #     errors["class"] = "Invalid Class."
            # allBackgrounds = ""
            # for background in allBackgroundsAPI:
            #     allBackgrounds += background
            # if postData['background'] not in allBackgrounds:
            #     errors["background"] = "Invalid Background."
            # allRaces = ""
            # for race in allRacesAPI:
            #     allRaces += race
            # if postData['race'] not in allRaces:
            #     errors["race"] = "Invalid Race."
        return errors        

class User(models.Model):
    firstName = models.CharField(max_length=17)
    lastName = models.CharField(max_length=17)
    username = models.CharField(max_length=50)
    password = models.TextField()
    dm = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    # RELATIONSHIPS

class Character(models.Model):
    # REQUIRED FIELDS
    name = models.CharField(max_length=17)
    charClass = models.CharField(max_length=17)
    level = models.IntegerField()
    background = models.CharField(max_length=17)
    race = models.CharField(max_length=17)
    ac = models.IntegerField()
    # OPTIONAL/EDITABLE FIELDS
        # Character Stats
    strength = models.IntegerField()
    dexterity = models.IntegerField()
    constitution = models.IntegerField()
    intelligence = models.IntegerField()
    wisdom = models.IntegerField()
    charisma = models.IntegerField()
        # Saving Throw Proficiency
    strSave = models.BooleanField()
    dexSave = models.BooleanField()
    conSave = models.BooleanField()
    intSave = models.BooleanField()
    wisSave = models.BooleanField()
    chaSave = models.BooleanField()
    # META DATA
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CharacterManager()
    # RELATIONSHIPS
    owner = models.ForeignKey(User, related_name="characters", on_delete = models.CASCADE)