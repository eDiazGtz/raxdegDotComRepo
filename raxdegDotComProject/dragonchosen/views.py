from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Hero, Monster, Saves, Speeds, DamageResistances, Senses, Traits, Actions
import bcrypt, urllib.request, json

# Create your views here.
def landing(request):
    return redirect('/dragonchosen')

def home(request):
    # CHECK LOGIN
    if 'userId' in request.session:
        user = User.objects.get(id=request.session['userId'])
        context = {
            "user":user,
        }
        return render(request, "home.html", context)
    return render(request, "home.html")

# ----------------- LOGIN & REGISTRATION --------------------------
def login(request):
    if 'userId' in request.session:
        user = User.objects.get(id=request.session['userId'])
        context = {
            "user":user,
        }
        return render(request, "login.html", context)
    return render(request, "login.html")

def loginUser(request):
    if(request.method == "POST"):
        errors = User.objects.loginValidator(request.POST)
        if User.objects.errorsPresent(errors, request):
            return redirect('/dragonchosen/login')
        else:
            user = User.objects.filter(username=request.POST['username'])
            user = user[0]
            request.session['userId'] = user.id
            messages.success(request, f"Welcome back, Dragonchosen {user.firstName}. The world was faltering without you.")
            return redirect('/dragonchosen')
    return redirect('/dragonchosen/login')

def register(request):
    if(request.method == "POST"):
        errors = User.objects.registrationValidator(request.POST)
        if User.objects.errorsPresent(errors, request):
            return redirect('/dragonchosen/login')
        else:
            hashpw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
            newUser = User.objects.create(firstName=request.POST['firstName'],lastName=request.POST['lastName'],username=request.POST['username'],password=hashpw,dm=False)
            request.session['userId'] = newUser.id
            messages.success(request, f"Welcome, Dragonchosen {newUser.firstName}. The fate of the world is in your hands now.")
            return redirect('/dragonchosen')
    return redirect('/dragonchosen/login')

def logout(request):
    request.session.flush()
    return redirect('/dragonchosen/login')

#  --------------------- USER EDITING ---------------------------------------

def editUser(request):
    errors = User.objects.isLoggedIn(request.session)
    if User.objects.errorsPresent(errors, request):
        return redirect('/dragonchosen/login')
    user = User.objects.get(id=request.session['userId'])
    context = {
        "user":user,
    }
    return render(request, "editUser.html", context)

def updateUser(request):
    errors = User.objects.isLoggedIn(request.session)
    if User.objects.errorsPresent(errors, request):
        return redirect('/dragonchosen/login')
    user = User.objects.get(id=request.session['userId'])
    errors = User.objects.updateValidator(request.POST, user.username)
    if User.objects.errorsPresent(errors, request):
        return redirect('/dragonchosen/edit')
    user.firstName = request.POST['firstName']
    user.lastName = request.POST['lastName']
    user.username = request.POST['username']
    user.dm = request.POST['dm']
    user.save()
    messages.success(request, f"Info Updated, Dragonchosen {user.firstName}!")
    return redirect(f"/dragonchosen/edit")

def editPassword(request):
    errors = User.objects.isLoggedIn(request.session)
    if User.objects.errorsPresent(errors, request):
        return redirect('/dragonchosen/login')
    user = User.objects.get(id=request.session['userId'])
    context = {
        "user":user,
    }
    return render(request, "editPassword.html", context)

def updatePassword(request):
    errors = User.objects.isLoggedIn(request.session)
    if User.objects.errorsPresent(errors, request):
        return redirect('/dragonchosen/login')
    if(request.method == "POST"):
        user = User.objects.get(id=request.session['userId'])
        errors = User.objects.passwordValidator(request.POST, user)
        if User.objects.errorsPresent(errors, request):
            return redirect(f'/dragonchosen/password')
        hashpw = bcrypt.hashpw(request.POST['passwordNew'].encode(), bcrypt.gensalt()).decode()
        user.password = hashpw
        user.save()
        messages.success(request, f"Password Updated, Dragonchosen {user.firstName}!")
    return redirect(f'/dragonchosen/edit')

def deleteUser(request):
    errors = User.objects.isLoggedIn(request.session)
    if User.objects.errorsPresent(errors, request):
        return redirect('/dragonchosen/login')
    user = User.objects.get(id=request.session['userId'])
    user.delete()
    request.session.flush()
    return redirect('/dragonchosen')

#  --------------------- USER EDITING ---------------------------------------


def heroes(request):
    errors = User.objects.isLoggedIn(request.session)
    if User.objects.errorsPresent(errors, request):
        return redirect('/dragonchosen/login')
    user = User.objects.get(id=request.session['userId'])
    heroes = Hero.objects.all()
    context = {
        "heroes":heroes,
        "user":user,
    }
    return render(request, "heroes.html", context)

def populateHeroes(request):
    with urllib.request.urlopen("http://www.larvalnemesis.com/naga/api/publicCharacterSummary") as url:
        heroes = json.loads(url.read().decode())
    #Once Heroes Loaded, Create List of NagaIds
    allHeroIds = []
    for existingHero in Hero.objects.all():
            allHeroIds.append(existingHero.nagaId)
    #Update or Create Hero    
    for hero in heroes:
        if len(allHeroIds) > 0:
            if hero['NagaId'] in allHeroIds:
                #Update Hero
                thisHero = Hero.objects.get(nagaId=hero['NagaId'])
                thisHero.name = hero['Name']
                thisHero.ac = hero['AC']
                thisHero.hp = hero['HP']
                thisHero.race = hero['Race']
                thisHero.level = hero['Level']
                thisHero.charClass = hero['Class']
                thisHero.passivePerception = hero['Passive Perception']
                thisHero.speed = hero['Speed']
                thisHero.alignment = hero['Alignment']
                thisHero.save()
                messages.success(request, f"IMPRESSIVE... MOST IMPRESSIVE")
            else:
                # Create Hero
                newHero = Hero.objects.create(name=hero['Name'],ac=hero['AC'],hp=hero['HP'],race=hero['Race'],level=hero['Level'],charClass=hero['Class'],passivePerception=hero['Passive Perception'],speed=hero['Speed'],alignment=hero['Alignment'],nagaId=hero['NagaId'],owner=User.objects.get(id=request.session['userId']))
                messages.success(request, f"A NEW CHALLENGER APPROACHES")
        else:
            # Create Hero
            newHero = Hero.objects.create(name=hero['Name'],ac=hero['AC'],hp=hero['HP'],race=hero['Race'],level=hero['Level'],charClass=hero['Class'],passivePerception=hero['Passive Perception'],speed=hero['Speed'],alignment=hero['Alignment'],nagaId=hero['NagaId'],owner=User.objects.get(id=request.session['userId']))
            messages.success(request, f"A NEW CHALLENGER APPROACHES")
    return redirect('/dragonchosen')

    #  --------------------- CAMPAIGN ---------------------------------------

def campaign(request):
# CHECK LOGIN
    if 'userId' in request.session:
        user = User.objects.get(id=request.session['userId'])
        context = {
            "user":user,
        }
        return render(request, "campaign.html", context)
    return render(request, "campaign.html")

def monsterEncounter(request):
    #TODO PATH VARIABLE FOR ENCOUNTER ID


    #What do we do if someone is NOT logged in?
    # if 'userId' in request.session:
    #     user = User.objects.get(id=request.session['userId'])

    #TODO Model for Encounter -- List of Monsters and a String for Encounter Name. Possibly an amount of Monster per monster chosen. 
    # thisEncounter = Encounter.objects.get(id=encounterId)
    blackAbishai = Monster.objects.get(name="black-abishai")
    context = {
        # "user":user,
        # "thisEncounter":thisEncounter,
        "monster":blackAbishai,
    }
    return render(request, "encounter.html", context)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    #  --------------------- MONSTERS ---------------------------------------

def getMonsters(request):

    json_data = open('D:/RaxdegDotCom/raxdegDotComProject/dragonchosen/static/json/monsters.json')   
    monsterFile = json.load(json_data) # deserialises it

    for key, dictOfDict in monsterFile.items():
        if key == "categories":
            continue
        for monName, monster in dictOfDict.items():
            monsterName = monName
            findMon = Monster.objects.filter(name=monName)
            if len(findMon) > 0:
                continue
            else:
                newMonster = Monster.objects.create(name=monsterName,ac=monster['ac'],creatureType=monster['type'],hpAvg=monster['hp_avg'],hp=monster['hp'],intValue=monster['int'],wisValue=monster['wis'],chaValue=monster['cha'],dexValue=monster['dex'],strValue=monster['str'],conValue=monster['con'],intBonus=monster['int_bonus'],wisBonus=monster['wis_bonus'],chaBonus=monster['cha_bonus'],dexBonus=monster['dex_bonus'],strBonus=monster['str_bonus'],conBonus=monster['con_bonus'],source=monster['source'],pageNumber=monster['page_number'])

                if "speeds" in monster:
                    for speed in monster['speeds']:
                        if len(Speeds.objects.all()) == 0:
                            newSpeed = Speeds.objects.create(content=speed)
                            newSpeed.monOwners.add(newMonster)
                        else:
                            findMe = Speeds.objects.filter(content=speed)
                            if len(findMe) == 0:
                                newSpeed = Speeds.objects.create(content=speed)
                                newSpeed.monOwners.add(newMonster)
                            else:
                                monSpeed = Speeds.objects.get(content=speed)
                                monSpeed.monOwners.add(newMonster)

                if "saves" in monster:
                    for save in monster['saves']:
                        if len(Saves.objects.all()) == 0:
                            newSave = Saves.objects.create(content=save)
                            newSave.monOwners.add(newMonster)
                        else:
                            findMe = Saves.objects.filter(content=save)
                            if len(findMe) == 0:
                                newSave = Saves.objects.create(content=save)
                                newSave.monOwners.add(newMonster)
                            else:
                                monSaves = Saves.objects.get(content=save)
                                monSaves.monOwners.add(newMonster)
                
                if "damage_resistances" in monster:
                    for damageResistances in monster['damage_resistances']:
                        if len(DamageResistances.objects.all()) == 0:
                            newDamageResistance = DamageResistances.objects.create(content=damageResistances)
                            newDamageResistance.monOwners.add(newMonster)
                        else:
                            findMe = DamageResistances.objects.filter(content=damageResistances)
                            if len(findMe) == 0:
                                newDamageResistance = DamageResistances.objects.create(content=damageResistances)
                                newDamageResistance.monOwners.add(newMonster)
                            else:
                                monDamageResistances = DamageResistances.objects.get(content=damageResistances)
                                monDamageResistances.monOwners.add(newMonster)
                
                if "senses" in monster:
                    for senses in monster['senses']:
                        if len(Senses.objects.all()) == 0:
                            newSense = Senses.objects.create(content=senses)
                            newSense.monOwners.add(newMonster)
                        else:
                            findMe = Senses.objects.filter(content=senses)
                            if len(findMe) == 0:
                                newSense = Senses.objects.create(content=senses)
                                newSense.monOwners.add(newMonster)
                            else:
                                monSenses = Senses.objects.get(content=senses)
                                monSenses.monOwners.add(newMonster)

                if "traits" in monster:
                    for trait in monster['traits']:
                        if len(Traits.objects.all()) == 0:
                            newTrait = Traits.objects.create(name=trait[0],content=trait[1]) 
                            newTrait.monOwners.add(newMonster)
                        else:
                            findMe = Traits.objects.filter(name=trait[0])
                            if len(findMe) == 0:
                                newTrait = Traits.objects.create(name=trait[0],content=trait[1]) 
                                newTrait.monOwners.add(newMonster)
                            else:
                                monTraits = Traits.objects.get(name=trait[0])
                                monTraits.monOwners.add(newMonster)
                
                if "actions_data" in monster:
                    for action in monster['actions_data']:
                        if len(Actions.objects.all()) == 0:
                            newAction = Actions.objects.create(parenthetical=action['parenthetical'],name=action['name'],content=action['description'])
                            newAction.monOwners.add(newMonster)
                        else:
                            findMe = Actions.objects.filter(name=action['name'])
                            if len(findMe) == 0:
                                newAction = Actions.objects.create(parenthetical=action['parenthetical'],name=action['name'],content=action['description'])
                                newAction.monOwners.add(newMonster)
                            else:
                                monActions = Actions.objects.get(name=action['name'])
                                monActions.monOwners.add(newMonster)

                messages.success(request, f"A NEW EVIL CREEPS FROM THE SHADOWS")
    return redirect('/dragonchosen')
