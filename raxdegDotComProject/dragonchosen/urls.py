from django.urls import path
from .views import home, monsterEncounter, login, logout, register, loginUser, editUser, updateUser, editPassword, updatePassword, deleteUser, heroes, populateHeroes, campaign, getMonsters

urlpatterns = [
    path('', home, name='home'),
    # LOGIN/REGISTER
    path('login', login, name='login'),
    path('logout', logout, name='logout'),
    path('register', register, name='register'),
    path('login/user', loginUser, name='loginUser'),
    # USER SETTINGS
    path('edit', editUser, name='editUser'),
    path('update', updateUser, name='updateUser'),
    path('password', editPassword, name='editPassword'),
    path('updatePassword', updatePassword, name='updatePassword'),
    path('deleteUser', deleteUser, name='deleteUser'),
    #HERO SETTINGS
    path('heroes', heroes, name='heroes'),
    path('populateHeroes', populateHeroes, name='populateHeroes'),
    #CAMPAIGN
    path('campaign', campaign, name='campaign'),
    path('monsterEncounter', monsterEncounter, name='monsterEncounter'),
    #MONSTER SETTINGS
    # path('monsters', monsters, name='monsters'),
    path('getMonsters', getMonsters, name='getMonsters'),

]
