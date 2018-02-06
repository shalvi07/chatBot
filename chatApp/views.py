from pyramid.view import (
    view_config,
    view_defaults
    )
import requests
from utils import Listerner,Sender
import json
import uuid
import pymongo
import datetime
from chatApp.models import USERS_COLLECTION,MESSAGE_COLLECTION


# rport = 8080
@view_defaults(route_name='send')
class TutorialViews(object):
    def __init__(self, request):
        self.request = request
        self.view_name = 'TutorialViews'
        # print(self.request.matchdict['first'])
        # self.id = request.matchdict['first']

    @property
    def full_name(self):
        print "in full_name"
        first = self.request.matchdict['first']
        # last = self.request.matchdict['last']
        print first
        return first

    @view_config(route_name='home', renderer='home.pt')
    def home(self):
        print("In home")
        return {'page_title': 'Home View'}

    # Retrieving /howdy/first/last the first time
    @view_config(renderer='edit.pt')
    def hello(self):
        print("in hello")
        return {'page_title': 'Hello View','new_port':'self.id'}

    # Posting to /howdy/first/last via the "Edit" submit button
    @view_config(request_method='POST', renderer='edit.pt')
    def edit(self):
        print("in edit")
        new_port = self.request.params['new_port']
        print(new_port)
        rport=new_port
        # listen=Listerner()
        # listen.listerner(6543)
        # send = Sender()
        # send.sender()
        print("here")
        return {'page_title': 'Edit View', 'new_port': new_port}

    # Posting to /howdy/first/last via the "Delete" submit button
    # @view_config(request_method='POST', request_param='form.delete',
    #              renderer='delete.pt')
    # def delete(self):
    #     print ('Deleted')
    #     return {'page_title': 'Delete View'}


    # @view_config(request_method='POST',
    #             request_param='form.message', renderer='message.pt')
    # def message(self):
    #     message=self.request.params['message']
    #     print(message)
    #     sendr=Sender()
    #     sendr.sender(message,6543,rport)
    #     listen=Listerner()
    #     listen.listerner(rport)
    #     return {'page_title': 'Message View', 'message': message}
    @view_config(route_name='chatbox',request_method = 'POST',
                request_param = 'form.message',renderer='chatbox.pt')
    def sendmessage(self):
        message=self.request.params['message']
        # print(message)
        # print full_name()
        print("in sendmessage")
        url="http://127.0.0.1:" + str(6543) +'/chatbox' +"/_john"
        data={'msg':message,'port':'6543'}
        data = json.dumps(data)

        r=requests.post(url,data=data)
        message_id=MESSAGE_COLLECTION.insert_one({"sender":"Smith",
                                                "receiver":"John",
                                                "message":message,
                                                "timestamp":datetime.datetime.utcnow()
                                                }).inserted_id

        print type(r),"qqqqqqqqq"
        print("message posted")

        return {'view_name':'XYX','page_title':'Message View',
                'message': message,'name':'_default'}




# @view_defaults(route_name="chatbox",renderer='chatbox.pt')
# class ChatBox:
    # def __init__(self,request):
    #     # print type(request),"in init func"
    #     # a = request.json_body
    #     # print a, "print request object"
    #     self.request=request
    #     self.view_name='ChatBox'
    #     # print type(self.request),"wwwwwww"
    #     print ()
a={}
print "shash"
@view_config(route_name='chatbox',
            request_method='GET',renderer='chatbox2.pt')
def receivedmessage(request):
    print "in get"
    # print('In receive')
    # url="http://127.0.0.1:" + str(rport) +'/chatbox'
    # r = requests.get(url)
    # print r
    # a = self.request.json_body
    print ("in recievemessage")
    print a
    msg= a.get('msg')
    print(msg)
    return {'view_name':'ChatBox','page_title':'Chatbox','message':msg}

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
    return {'view_name':'ChatBox','page_title':'Chatbox','message':str(msg)}
    # return msg

@view_config(route_name='chatbox',request_method='POST',
            renderer='chatbox2.pt',request_param='form.reply')
def sendreply(request):
    print ("in sendreply")
    message=request.params['message']
    # print(message)
    url="http://127.0.0.1:" + str(6543) +'/chatbox'+'/_default'
    data={'msg':message,'port':'8080'}
    data = json.dumps(data)
    r=requests.post(url,data=data)
    message_id=MESSAGE_COLLECTION.insert_one({"sender":"John",
                                            "receiver":"Smith",
                                            "message":message,
                                            "timestamp":datetime.datetime.utcnow()
                                            }).inserted_id
    return {'view_name':'ChatBox','page_title':'Chatbox',
            'message':str(message)}



@view_config(route_name='history',request_method='GET',
            renderer='history.pt')
def history(request):
    reciever = request.url[36:]
    message=MESSAGE_COLLECTION.find({"sender":"Smith",
                                "receiver":"John"}).sort(
                                'timestamp',pymongo.DESCENDING)
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
