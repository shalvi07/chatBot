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
EndPoint to send and view messages between sender and receiver.
For eg: http://localhost:6543/chatbox/Smith/John opens chatbox for Smith. Smith will now be able to send message to John through post request and view messages between them using get request.

By Default Get request would return 5 most recent message. If the user wants to see more messages, he/she passes a parameter in request __numsrollup__ which has an **Integer** value as in number of times the user clicks on the scrool up button, by default its value is assumed to be 1, If user clicks for the first time the value passed should be 2 the GET request thus made would return 10 messages, if the user presses the scrollup button again value of __numscrollup__ should now be passed 3, the request thus made will return 15 messages and so on..
John will be able to see the message at http://localhost:6543/chatbox/John/Smith

Request: 
         Get : Params: sender,receiver,numsrcollup(optional)
         Displays most recent messages (5) received or sent in between the user.
            
         Post : Params: sender, receiver
                Body: message
        Posts the message from sender to the receiver
Response:
        Get: message and HTTP status.
        Post: Message and HTTP status.
    
 Sender and Receiver are parameters to url.   
## http://localhost:6543/inbox/{username}

Displays unread messages user has received.
Once the user sees a message through get request at /chatbox/username/sender it is no more displayed at /inbox
Request: 
         Get : Params: username
                
                        
Response:
        Get: list of messages and HTTP status

## http://localhost:6543/broadcast/{sender}

Endpoint to post message to multiple receivers. List of receivers in passed as list through the body of the post request.
Request: 
         Post : Params: sender
                Body:   message
                        receiver(list)
                        
Response:
        Post: Message,ResponseMessage and HTTP status

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
