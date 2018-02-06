# chatBot
## overview
Simple chat appllication with peer to peer communication.

##Tech Stack

Uses pyramid framework.
MongoDB as Database.

##Endpoints

## http://localhost:6543/home
Options to select user to send message

##http://localhost:6543/chatbox/_Smith
Displays most recent message received and a text box to send reply
For eg: http://localhost:6543/chatbox/_Smith opens chatbox for Smith. Assuming Smith selected John from home page,he sends message to John. John will be able to see the message at http://localhost:6543/chatbox/_John.

##http://localhost:6543/history/Smith_John
Displays history of messages send between Smith and any other user.

Note: Smith is the default user assumed starting the application. Changing default user can be added in next interation.
