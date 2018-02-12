from pyramid.view import (
    view_config,
    view_defaults
    )
from pyramid.response import Response
from pyramid.config import Configurator
import requests
from utils import Listerner,Sender,Utils
import json
import uuid
import pymongo
import datetime
from dateutil import tz
from chatApp.models import USERS_COLLECTION,MESSAGE_COLLECTION


Utilobj= Utils()
receiver = "John"
sender = 'Smith'
a={}
temp='chatbox.pt'
print "shash"
users = USERS_COLLECTION.find()
userlist = list()
for record in users:
    userlist.append(record['name'])

class ChatViews(object):
    def __init__(self, request):
        self.request = request
        self.view_name = 'ChatApp'

    @view_config(route_name='home', renderer='home.pt')
    def home(self):
        global receiver
        print self.request
        print("In home")
        return {'page_title': 'Home View'}

    @view_config(route_name='chatbox',request_method = 'POST')
    def sendmessage(self):
        print("in sendmessage")
        sender = self.request.matchdict.get('sender')
        receiver = self.request.matchdict.get('receiver')

        if Utilobj.userexits(sender) and Utilobj.userexits(receiver):
            try:
                message = self.request.json_body['message']
            except ValueError:
                resp =  Response(body=json.JSONEncoder().encode({'message':
                                                                'Please enter MEssage',
                                                                'sender':sender,
                                                                'receiver':receiver}),
                                status=500, content_type='application/json')
                return resp

            print receiver

            message_id=MESSAGE_COLLECTION.insert_one({"sender":sender,
                                                "receiver":receiver,
                                                "message":message,
                                                "timestamp":datetime.datetime.utcnow()
                                                }).inserted_id
            print("message posted")
            resp =  Response(body=json.JSONEncoder().encode({'message': message,
                                                            'sender':sender,
                                                            'receiver':receiver}),
                            status=200, content_type='application/json')
            return resp
        else:
            resp = Response(body=json.JSONEncoder().encode({'message': 'User does not exit',
                                                            'sender':sender,
                                                            'receiver':receiver}),
                            status=422, content_type='application/json')
            return resp




@view_config(route_name='chatbox',request_method='GET')
def receivedmessage(request):
    print "in get"
    print request
    print request.matchdict.get('sender'), ">>>>>>>>>."
    sender = request.matchdict.get('sender')
    receiver = request.matchdict.get('receiver')
    print type(request)
    if Utilobj.userexits(sender) and Utilobj.userexits(receiver):
        recentmessagelist = list()
        recentmessages = MESSAGE_COLLECTION.find({'$or':[{"sender":sender,"receiver":receiver},
                                                        {"sender":receiver,"receiver":sender}
                                                        ]}).sort('timestamp',pymongo.DESCENDING).limit(5)
        for record in recentmessages:


            # print temp
            # temp = temp.replace(tzinfo=from_zone)
            # print temp
            temp = Utilobj.convert_to_local_tz(record['timestamp'])
            draft={
                    'message':record['message'],
                    'sender': record['sender'],
                    'receiver':record['receiver'],
                    'timestamp':temp.strftime("%Y-%m-%d %H:%M:%S")
                    }
            recentmessagelist.append(draft)
        resp = Response(body=json.JSONEncoder().encode(recentmessagelist),
                        status=200, content_type='application/json')
        return resp
    else:
        resp = Response(body=json.JSONEncoder().encode({'message': 'User does not exit',
                                                        'sender':sender,'receiver':receiver}),
                        status=422, content_type='application/json')
        return resp



@view_config(route_name='history',request_method='GET')
def history(request):
    first = request.matchdict.get('first')
    second = request.matchdict.get('second')
    print receiver
    if Utilobj.userexits(first) and Utilobj.userexits(second):
        print 'hereeeeee'
        message=MESSAGE_COLLECTION.find({'$or': [{"receiver":first,"sender":second},
                                                {"sender":first,"receiver":second}]
                                                }).sort('timestamp',pymongo.DESCENDING)
        msghistory = list()
        for record in message:
            temp = Utilobj.convert_to_local_tz(record['timestamp']).strftime("%Y-%m-%d %H:%M:%S")
            draft={
                    'message':record['message'],
                    'sender': record['sender'],
                    'receiver':record['receiver'],
                    'timestamp':temp
                    }
            msghistory.append(draft)
        resp = Response(body=json.JSONEncoder().encode(msghistory),
                        status=200, content_type='application/json')
        return resp

    else:
        resp = Response(body=json.JSONEncoder().encode({'message': 'User does not exit',
                                                        'sender':sender,'receiver':receiver}),
                        status=422, content_type='application/json')
        return resp
