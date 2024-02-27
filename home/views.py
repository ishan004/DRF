from rest_framework.decorators import api_view
from rest_framework.response import Response
from home.serializers import PeopleSerializer , LoginSerializer
from home.models import Person

from turtle import color
from functools import partial
from rest_framework.views import APIView

# Create your views here.


@api_view(['GET', 'POST', 'PUT'])
def index(request):
    course = { 
              'course_name': 'Python',
              'learn': ['flask', 'Django', 'Tornado', 'FastApi'],
              'course_provider': 'Scaler'
                  }
    if request.method == 'GET':
        print(request.GET.get('search'))
        print('You Hit a GET method')
        return Response(course)
    elif request.method == 'POST':
        data =request.data
        print('****')
        print(data['age'])
        print('****')
        print('You Hit a POST method')
        return Response(course)
    elif request.method == 'PUT':
        print('You Hit a PUT method')
        return Response(course)
    
    
@api_view(['POST'])
def login(request):
    data = request.data
    serializer = LoginSerializer(data=data)
    
    if serializer.is_valid():
        data = serializer.data
        print(data)
        return Response({'message':'Success'})
        
        
    return Response(serializer.errors)


class PersonAPI(APIView):
    
    def get(self,  request):
        objs = Person.objects.filter(color__isnull=False)
        serializer = PeopleSerializer(objs, many =True)
        return Response(serializer.data)
    
    def post(self, request):
        data=request.data
        serializer = PeopleSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

    def put(self, request):
        data = request.data
        serializer = PeopleSerializer(data =data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
    
    def patch(self, request):
        data = request.data
        obj = Person.objects.get(id=data['id'])
        serializer = PeopleSerializer(obj,data =data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors)
    
    def delete(self, request):
        data = request.data
        obj = Person.objects.get(id=data['id'])
        obj.delete()
        return Response({'message':'Person was deleted'})
    
    
@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])        
def person(request):
    if request.method == 'GET':
        
        objs = Person.objects.filter(color__isnull=False)
        serializer = PeopleSerializer(objs, many =True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        data=request.data
        serializer = PeopleSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors)
    
    elif request.method == "PUT":
        data = request.data
        serializer = PeopleSerializer(data =data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors)
    
    elif request.method == "PATCH":
        data = request.data
        obj = Person.objects.get(id=data['id'])
        serializer = PeopleSerializer(obj,data =data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors)
    
    else:
        data = request.data
        obj = Person.objects.get(id=data['id'])
        obj.delete()
        return Response({'message':'Person was deleted'})