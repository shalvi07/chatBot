# chatBot
# overview
Simple chat appllication with peer to peer communication.

#Tech Stack

Uses pyramid framework.
MongoDB as Database.

#Endpoints

/home : Options to select user to send message
#/chatbox/_<user>
Displays most recent message received and a text box to send reply
For eg: /chatbox/_Smith
opens chatbox for smith. Assuming Smith selected John from home page,he sends message to John. John will be able to see the message at /chatbox/_John.

/history/Smith_<receiver>: Displays history of messages send between Smith and any other user.

Note: Smith is the default user assumed starting the application. Changing default user can be added in next interation.
