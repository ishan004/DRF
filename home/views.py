from rest_framework.decorators import api_view
from rest_framework.response import Response
from home.serializers import PeopleSerializer , LoginSerializer, RegisterSerializer
from home.models import Person
from turtle import color
from functools import partial
from rest_framework.views import APIView
from rest_framework import viewsets , status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from django.core.paginator import Paginator


class LoginAPI(APIView):
    
    def post(self, request):
        data = request.data
        serializer = LoginSerializer(data = data)
        if not serializer.is_valid():
            return Response({
                'status': False,
                'message': serializer.errors
            }, status.HTTP_400_BAD_REQUEST)
        
        
        user = authenticate(username= serializer.data['username'], password= serializer.data['password'])
        if not user:
            return Response({
                'status': False,
                'message': 'invalid credentials'
            }, status.HTTP_400_BAD_REQUEST)
        token = Token.objects.get_or_create(user=user)
        return Response({'status': True, 'message': 'user login', 'token':str(token)}, status.HTTP_201_CREATED)

class RegisterAPI(APIView):
    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data =data)
        
        if not serializer.is_valid():
            return Response({
                'status': False,
                'message': serializer.errors
            }, status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return Response({'status': True, 'message': 'user created'}, status.HTTP_201_CREATED)

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
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    
    def get(self,  request):
        try:
            print(request.user)
            objs = Person.objects.all()
            page = request.GET.get('page', 1)
            page_size = 3
        
            paginator = Paginator(objs, page_size)
        
            serializer = PeopleSerializer(paginator.page(page), many =True)
            return Response(serializer.data)

        except:
            return Response({'status':False,
                             'message':'invalid page number'})
    
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
    
    
class PeopleViewSet(viewsets.ModelViewSet):
    serializer_class = PeopleSerializer
    queryset = Person.objects.all()
    
    def list(self, request):
        search = request.GET.get('search')
        queryset = self.queryset
        if search:
            queryset = queryset.filter(name__startswith = search)
        
        serializer = PeopleSerializer(queryset, many=True)
                                 
        return Response({'status':200, 'data':serializer.data})