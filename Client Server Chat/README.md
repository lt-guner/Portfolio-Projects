# Project 4 - Client-Server Chat

Introduction ![](Aspose.Words.170c0f87-21c8-4277-9058-c6b2c11da437.001.png)

In this coding project you will write a simple client-server program using python sockets. Your program will emulate a simple chat client. For extra-credit (points tbd), turn your chat program into a simple ascii multiplayer game (see below for spec). 

Writing a client-server socket program ![](Aspose.Words.170c0f87-21c8-4277-9058-c6b2c11da437.002.png)

This chat client-server is fairly simple in design. The server doesn’t handle multiple clients, and there is only one socket connection made. You will reuse this socket for the life of the program. The one issue with reusing sockets is that there is no easy way to tell when you’ve received a complete communication: 

“… if you plan to reuse your socket for further transfers, you need to realize that *there is* 

*no* EOT (end of transmission) *on a socket.* I repeat: if a socket send or recv returns after handling 0 bytes, the connection has been broken. If the connection has *not* been broken, you may wait on a recv forever, because the socket will *not* tell you that there’s nothing more to read (for now). Now if you think about that a bit, you’ll come to realize a fundamental truth of sockets: *messages must either be fixed length* (yuck), *or be delimited* (shrug), *or indicate how long they are* (much better), *or end by shutting down the connection*. The choice is entirely yours, (but some ways are righter than others).”

*Source: [ https://docs.python.org/3.4/howto/sockets.html* ](https://docs.python.org/3.4/howto/sockets.html)*

Note that in the process of testing, you can “hang” a port. This will give an error when you start the server:![](Aspose.Words.170c0f87-21c8-4277-9058-c6b2c11da437.003.png)[ \[Errno 48\] Address already in use.](https://stackoverflow.com/questions/19071512/socket-error-errno-48-address-already-in-use) Don’t worry, the ports will recycle eventually. 

There are several ways around this, including simply specifying a different port every time you run. A good alternative, that mostly works, is to set a socket reuse option before the bind command on the server:  s.setsockopt(socket.SOL\_SOCKET, socket.SO\_REUSEADDR, 1)

Specification ![](Aspose.Words.170c0f87-21c8-4277-9058-c6b2c11da437.004.png)Server ![](Aspose.Words.170c0f87-21c8-4277-9058-c6b2c11da437.005.png)

1. The server creates a socket and binds to ‘localhost’ and port xxxx 
1. The server then listens for a connection 
1. When connected, the server calls recv to receive data 
1. The server prints the data, then prompts for a reply 
5. If the reply is /q, the server quits 
5. Otherwise, the server sends the reply 
5. Back to step 3 
5. Sockets are closed (can use *with* in python3) ![](Aspose.Words.170c0f87-21c8-4277-9058-c6b2c11da437.006.png)

Client ![](Aspose.Words.170c0f87-21c8-4277-9058-c6b2c11da437.007.png)

1. The client creates a socket and connects to ‘localhost’ and port xxxx 
1. When connected, the client prompts for a message to send 
1. If the message is /q, the client quits 
1. Otherwise, the client sends the message 
1. The client calls recv to receive data 
1. The client prints the data 
1. Back to step 2 
1. Sockets are closed (can use *with* in python3) ![](Aspose.Words.170c0f87-21c8-4277-9058-c6b2c11da437.008.png)

A better spec might just be to show example screenshots: 



|<p>![](Aspose.Words.170c0f87-21c8-4277-9058-c6b2c11da437.009.png)</p><p>![](Aspose.Words.170c0f87-21c8-4277-9058-c6b2c11da437.010.png)</p>|
| - |
|<p>What to turn in </p><p>1. In the Word doc: </p><p>a. Include instructions on how to run your programs. Are they python3?**  </p><p>b. Include screenshots of your running code. </p><p>c. Include comments / questions (optional) </p><p>2. In your code listings: </p><p>a. Include sources you used (web pages, tutorials, books, etc) </p><p>b. Comment your code </p>|
Extra Credit 

Turn your client-server into a multiplayer ascii game. Tic-tac-toe? Hangman? The choice is up to you. Points awarded subjectively based on effort. 5 extra points possible. 

Resources ![](Aspose.Words.170c0f87-21c8-4277-9058-c6b2c11da437.011.png)[https://docs.python.org/3.4/howto/sockets.html ](https://docs.python.org/3.4/howto/sockets.html)[https://realpython.com/python-sockets/ ](https://realpython.com/python-sockets/)![](Aspose.Words.170c0f87-21c8-4277-9058-c6b2c11da437.012.png)
