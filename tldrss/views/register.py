import json

from django.http import HttpResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

from rest_framework.authentication import authenticate
from rest_framework.authtoken.models import Token


@csrf_exempt
def register_user(request):
    '''Handle creation of new user for authentication

    Method arguments:
        request -- The full HTTP request object
    '''

    # load JSON string of request body into a dict
    req_body = json.loads(request.body.decode())


    # create new user
    new_user = User.objects.create_user(
        username=req_body['username'],
        email=req_body['email'],
        password=req_body['password'] 
    )

    # REST framework token generator
    token = Token.objects.create(user=new_user)

    # return data to client
    data = json.dumps({'token': token.key})

    return HttpResponse(data, content_type='application/json')

@csrf_exempt
def login_user(request):
    ''' Handle user authentication

    Method arguments:
        request -- full HTTP request object
    '''

    # load JSON string of request body into a dict
    req_body = json.loads(request.body.decode())

    if request.method == 'POST':

        username = req_body['username']
        password = req_body['password']
        authenticated_user = authenticate(username=username, password=password)

        if authenticated_user is not None:
            token = Token.objects.get(user=authenticated_user)
            data = json.dumps({'valid': True, 'token': token.key})
            return HttpResponse(data, content_type='application/json')

        else:
            # invalid login credentials
            data = json.dumps({'valid': False})
            return HttpResponse(data, content_type='application/json')