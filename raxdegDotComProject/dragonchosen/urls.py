from django.urls import path
from .views import home, darkabishai, login, logout, register, loginUser, editUser, updateUser, editPassword, updatePassword, deleteUser

urlpatterns = [
    path('', home, name='home'),
    path('darkabishai', darkabishai, name='darkabishai'),
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

]
