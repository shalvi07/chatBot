# chatBot
## overview
Simple chat appllication with peer to peer communication.

## Tech Stack

Uses pyramid framework.
MongoDB as Database.

## Endpoints

## http://localhost:6543/home
__Home Page__ with options to select user to send message

## http://localhost:6543/chatbox/
Displays most recent message received and a text box to send reply
For eg: http://localhost:6543/chatbox/_Smith opens chatbox for Smith. Assuming Smith(default user) selects John from home page,he would send message to John. John will be able to see the message at http://localhost:6543/chatbox/_John.

## http://localhost:6543/history/
Displays history of messages send between Smith and any other user.
for eg http://localhost:6543/history/Smith_John gives history of chat between Smith and John.
Similarly http://localhost:6543/history/Smith_Helen gives chat history between Smith and John. Smith is by default (and as of now only) the first person.

__Note__: Smith is by default(and as of now only) the first user since login logout feature is not supported. Changing default user can be added in next interation. First user is the user who starts the application and sends message to the other user(Second user).Multiple Second users supported.
