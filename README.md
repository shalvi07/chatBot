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
Response : HTML Page (home.pt)

## http://localhost:6543/chatbox/{sender}/{receiver}
Displays most recent message received or sent and a text box to send reply
For eg: http://localhost:6543/chatbox/Smith opens chatbox for Smith. Assuming Smith(default user) selects John from home page,he would send message to John. John will be able to see the message at http://localhost:6543/chatbox/\_John.

Request: 
         Get : Params: sender,receiver
         Displays most recent messages (5) received or sent in between the user.
            
         Post : Params: sender, receiver
                Body: message
        Posts the message from sender to the receiver
Response:
        Get: message and HTTP status.
        Post: Message and HTTP status
    
 Sender and Receiver are parameters to url.   

## http://localhost:6543/history/{firstperson}/{secondperson}
Displays history of messages send between any two user existing in database
for eg http://localhost:6543/history/Smith_John gives history of chat between Smith and John.
Similarly http://localhost:6543/history/Smith_Helen gives chat history between Smith and Helen. Smith is by default (and as of now only) the first person.

Request: GET: parameters: firstperson, secondperson

Response: HTML page with complete chat history.
firstperson, secondperson is the parameter to endpoint



## Install Notes
1. Fork and clone the repo.
2. Install mongodb
3. Install and set up a virtual environment
4. Setup a dummy db.
5. Run following commands
    1. cd chatBot
    2. pip install -e .
    3. pserve development.ini --reload
