from home.views import index, person, login, PersonAPI
from django.urls import path , include

urlpatterns = [
    path('index/', index),
    path('person/',person),
    path('login/', login),
    path('persons/',PersonAPI.as_view())
]

