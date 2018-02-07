from pyramid.view import (
    view_config,
    view_defaults
    )
from pyramid.config import Configurator
import requests
from utils import Listerner,Sender
import json
import uuid
import pymongo
import datetime
from chatApp.models import USERS_COLLECTION,MESSAGE_COLLECTION

receiver = "John"


class ChatViews(object):
    def __init__(self, request):
        self.request = request
        self.view_name = 'ChatApp'

    @view_config(route_name='home', renderer='home.pt')
    def home(self):
        global receiver
        print self.request.params
        print("In home")
        return {'page_title': 'Home View'}

    @view_config(route_name='chatbox',request_method = 'POST',
                request_param = 'form.message',renderer='chatbox.pt')
    def sendmessage(self):
        message = self.request.params['message']
        # print(message)
        # print full_name()
        print("in sendmessage")
        url="http://127.0.0.1:" + str(6543) +'/chatbox' +"/_" + receiver
        data={'msg':message,'port':'6543'}
        data = json.dumps(data)

        r=requests.post(url,data=data)
        message_id=MESSAGE_COLLECTION.insert_one({"sender":"Smith",
                                                "receiver":receiver,
                                                "message":message,
                                                "timestamp":datetime.datetime.utcnow()
                                                }).inserted_id
        print type(r),"qqqqqqqqq"
        print("message posted")
        return {'view_name':'XYX','page_title':'Chatbox',
                'message': message,'name':'_Smith','show_form_message':True,
                'show_form_reply':False,'test':True}

a={}
temp='chatbox.pt'
print "shash"
users = USERS_COLLECTION.find()
userlist = list()
for record in users:
    userlist.append(record['name'])

@view_config(route_name='chatbox',request_method='GET',renderer='chatbox.pt')
def receivedmessage(request):
    print "in get"
    param = request.url[31:36]
    user = request.url[31:]
    print user
    print param
    if user in userlist or param in userlist:
        print user
        print param+"pS"
        test = True
        if param=='Smith':
            showSendMessage = True
            showSendReply = False
            # config.add_renderer(temp)
        else:
            showSendMessage = False
            showSendReply = True
    else:
        test = False
        showSendMessage = False
        showSendReply = False
    global receiver
    try:
        receiver = request.params['receiver']
    except KeyError:
        print "KeyError occured"
    print ("in recievemessage")
    print a
    print receiver
    msg= a.get('msg')
    print(msg)
    return {'view_name':'ChatBox','page_title':'Chatbox',
            'message':str(msg),'show_form_message':showSendMessage,
            'show_form_reply':showSendReply,'test':test}


@view_config(route_name='chatbox',
            request_method='POST',renderer='chatbox.pt')
def receivedmessage2(request):
    print('In receive22222')
    global a
    a = request.json_body
    msg = a.get('msg')
    print msg

    # url="http://127.0.0.1:" + str(rport) +'/message'
    # r = requests.post(url,)
    # print r
    return {'view_name':'ChatBox','page_title':'Chatbox','message':str(msg),
            'show_form_message':True,'show_form_reply':True,'test':True}
    # return msg

@view_config(route_name='chatbox',request_method='POST',
            renderer='chatbox.pt',request_param='form.reply')
def sendreply(request):
    print ("in sendreply")
    message=request.params['message']
    # print(message)
    url="http://127.0.0.1:" + str(6543) +'/chatbox'+'/_Smith'
    data={'msg':message,'port':'8080'}
    data = json.dumps(data)
    r=requests.post(url,data=data)
    print receiver
    message_id=MESSAGE_COLLECTION.insert_one({"sender":receiver,
                                            "receiver":"Smith",
                                            "message":message,
                                            "timestamp":datetime.datetime.utcnow()
                                            }).inserted_id
    return {'view_name':'ChatBox','page_title':'Chatbox',
            'message':str(message),'name':'_'+receiver,'show_form_message':False,
            'show_form_reply':True,'test':True}



@view_config(route_name='history',request_method='GET',
            renderer='history.pt')
def history(request):
    receiver = request.url[36:]
    print receiver
    message=MESSAGE_COLLECTION.find({'$or': [{"receiver":"Smith","sender":receiver},
                                            {"sender":"Smith","receiver":receiver}]
                                            }).sort('timestamp',pymongo.DESCENDING)
    msghistory = list()
    for record in message:
        draft={
                'message':record['message'],
                'sender': record['sender'],
                'receiver':record['receiver'],
                'timestamp':record['timestamp']
                }
        msghistory.append(draft)
    return {'msghistory':msghistory}
