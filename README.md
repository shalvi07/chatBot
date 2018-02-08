# chatBot
## overview
Simple chat appllication with peer to peer communication.

## Tech Stack

Uses pyramid framework.
MongoDB as Database.

## Endpoints

## http://localhost:6543/
__Home Page__ with options to select user to send message
Request: GET
Response :

## http://localhost:6543/chatbox/{_user}
Displays most recent message received or sent and a text box to send reply
For eg: http://localhost:6543/chatbox/\_Smith opens chatbox for Smith. Assuming Smith(default user) selects John from home page,he would send message to John. John will be able to see the message at http://localhost:6543/chatbox/\_John.

Request: Get : Params: form.message,receiver

         Post : Params: form.message, form.reply, message
                File: _{receiver}
    {_receiver} is the parameter to endpoint.   

## http://localhost:6543/history/{Sender_Receiver}
Displays history of messages send between Smith and any other user.
for eg http://localhost:6543/history/Smith_John gives history of chat between Smith and John.
Similarly http://localhost:6543/history/Smith_Helen gives chat history between Smith and Helen. Smith is by default (and as of now only) the first person.

Request: GET: File: {Sender_Receiver}

{Sender_Receiver} is the parameter to endpoint

__Note__: Smith is by default(and as of now only) the first user since login logout feature is not supported. Changing default user can be added in next interation. First user is the user who starts the application and sends message to the other user(Second user).Multiple Second users supported.


## Install Notes
1. Fork and clone the repo.
2. Install mongodb
3. Install and set up a virtual environment
4. Setup a dummy db.
5. Run following commands
    1. cd chatBot
    2. pip install -e .
    3. pserve development.ini --reload
