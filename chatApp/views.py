from pyramid.view import (
    view_config,
    view_defaults
    )
from pyramid.response import Response
from pyramid.config import Configurator
import requests
from utils import Listerner,Sender
import json
import uuid
import pymongo
import datetime
from dateutil import tz
from chatApp.models import USERS_COLLECTION,MESSAGE_COLLECTION
from_zone = tz.tzutc()
to_zone = tz.tzlocal()

# localtz = tzlocal.get_localzone()
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
        # print self.request
        # global userlist
        sender = self.request.matchdict.get('sender')
        receiver = self.request.matchdict.get('receiver')

        if userexits(sender,userlist) and userexits(receiver,userlist):
            try:
                message = self.request.json_body['message']
            except ValueError:
                resp =  Response(body=json.JSONEncoder().encode({'message':
                                                                'Please enter MEssage',
                                                                'sender':sender,
                                                                'receiver':receiver}),
                                status=500, content_type='application/json')
                return resp

        # url="http://127.0.0.1:" + str(6543) +'/chatbox/'+receiver+'/'+sender
        # data={'message':message}
        # data = json.dumps(data)
            print receiver

        # r=requests.post(url,data=data)
            message_id=MESSAGE_COLLECTION.insert_one({"sender":sender,
                                                "receiver":receiver,
                                                "message":message,
                                                "timestamp":datetime.datetime.utcnow()
                                                }).inserted_id
        # print type(r),"qqqqqqqqq"
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

        # return {'view_name':'XYX','page_title':'Chatbox',
        #         'message': message,'name':'_Smith','show_form_message':True,
        #         'show_form_reply':False,'test':True}



@view_config(route_name='chatbox',request_method='GET')
def receivedmessage(request):
    print "in get"
    print request
    print request.matchdict.get('sender'), ">>>>>>>>>."
    sender = request.matchdict.get('sender')
    receiver = request.matchdict.get('receiver')
    # param = request.url[31:36]
    # user = request.url[31:]
    # print user
    # print param
    print type(request)
    if userexits(sender,userlist) and userexits(receiver,userlist):
        recentmessagelist = list()
        recentmessages = MESSAGE_COLLECTION.find({'$or':[{"sender":sender,"receiver":receiver},
                                                        {"sender":receiver,"receiver":sender}
                                                        ]}).sort('timestamp',pymongo.DESCENDING).limit(5)
        for record in recentmessages:

            temp=record['timestamp']
            print temp
            temp = temp.replace(tzinfo=from_zone)
            print temp
            temp = temp.astimezone(to_zone)
            draft={
                    'message':record['message'],
                    'sender': record['sender'],
                    'receiver':record['receiver'],
                    'timestamp':temp.strftime("%Y-%m-%d %H:%M:%S")
                    }
            recentmessagelist.append(draft)
        # print user
        # print param+"pS"
        # test = True

        # if param=='Smith':
        #     showSendMessage = True
        #     showSendReply = False
        #     # config.add_renderer(temp)
        # else:
        #     showSendMessage = False
        #     showSendReply = True
        resp = Response(body=json.JSONEncoder().encode(recentmessagelist),
                        status=200, content_type='application/json')
        return resp
    else:
        resp = Response(body=json.JSONEncoder().encode({'message': 'User does not exit',
                                                        'sender':sender,'receiver':receiver}),
                        status=422, content_type='application/json')
        return resp
    # print ("in recievemessage")
    # print a
    # print receiver
    # msg= a.get('msg')
    # print(msg)
    # print "--------------"
    # resp =  Response(body=json.JSONEncoder().encode({'message': msg}), status=200, content_type='application/json')
    # return resp
    # return {'view_name':'ChatBox','page_title':'Chatbox',
            # 'message':str(msg),'show_form_message':showSendMessage,
            # 'show_form_reply':showSendReply,'test':test}

#
# @view_config(route_name='chatbox',
#             request_method='POST',renderer='chatbox.pt')
# def receivedmessage2(request):
#     print('In receive22222')
#     global a
#     print request.body
#     a = request.json_body
#     print a
#     msg = a.get('message')
#     print msg
#     return {'view_name':'ChatBox','page_title':'Chatbox','message':str(msg),
#             'show_form_message':True,'show_form_reply':True,'test':True}

# @view_config(route_name='chatbox',request_method='POST',
#             renderer='chatbox.pt',request_param='form.reply')
# def sendreply(request):
#     print ("in sendreply")
#     message=request.params['message']
#     # print(message)
#     url="http://127.0.0.1:" + str(6543) +'/chatbox'+'/_Smith'
#     data={'msg':message,'port':'8080'}
#     data = json.dumps(data)
#     r=requests.post(url,data=data)
#     print receiver
#     message_id=MESSAGE_COLLECTION.insert_one({"sender":receiver,
#                                             "receiver":"Smith",
#                                             "message":message,
#                                             "timestamp":datetime.datetime.utcnow()
#                                             }).inserted_id
#     return {'view_name':'ChatBox','page_title':'Chatbox',
#             'message':str(message),'name':'_'+receiver,'show_form_message':False,
#             'show_form_reply':True,'test':True}



@view_config(route_name='history',request_method='GET',
            renderer='history.pt')
def history(request):
    first = request.matchdict.get('first')
    second = request.matchdict.get('second')
    print receiver
    message=MESSAGE_COLLECTION.find({'$or': [{"receiver":first,"sender":second},
                                            {"sender":first,"receiver":second}]
                                            }).sort('timestamp',pymongo.DESCENDING)
    msghistory = list()
    for record in message:
        temp=record['timestamp']
        print temp
        temp = temp.replace(tzinfo=from_zone)
        print temp
        temp = temp.astimezone(to_zone).strftime("%Y-%m-%d %H:%M:%S")
        draft={
                'message':record['message'],
                'sender': record['sender'],
                'receiver':record['receiver'],
                'timestamp':temp
                }
        msghistory.append(draft)
    return {'msghistory':msghistory}


def userexits(user,userlist):
    if user in userlist:
        return True
    else:
        return False
