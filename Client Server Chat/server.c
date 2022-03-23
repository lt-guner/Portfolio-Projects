/* 
* Class: CS 372
* Term: Winter 22
* Assignment 4: client server chat
* Author: Timur Guner
*/

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/wait.h>
#include <netinet/in.h>
#include <netdb.h> 
#include <ctype.h>

void error(const char *msg) { perror(msg); exit(1); } // Error function used for reporting issues

int main(int argc, char *argv[]) {
	
	// if correct parameters are not passed then exit with error
	if (argc != 2) 
	{ 
		error("USAGE: ./server port#\n");
	} 

	// needed variables
	int listenSocket, portNumber, connectionSocket, charsRead, charsWritten;
	struct sockaddr_in serverAddress, clientAddress;
  	socklen_t sizeOfClientInfo = sizeof(clientAddress);
    char buffer_client[1024];
    char buffer_server[1024];

	// Clear out the address struct
    memset((char*)&serverAddress, '\0', sizeof(serverAddress));

	// The address should be network capable
    serverAddress.sin_family = AF_INET;

	 // Store the port number
    portNumber = atoi(argv[1]);
    serverAddress.sin_port = htons(portNumber);

	// Allow a client at any address to connect to this server
	serverAddress.sin_addr.s_addr = INADDR_ANY;

	// Create the socket that will listen for connections
	listenSocket = socket(AF_INET, SOCK_STREAM, 0);
	if (listenSocket < 0) 
	{
		error("SERVER: Error opening socket\n");
	}

	// Associate the socket to the port
	if (bind(listenSocket, (struct sockaddr *)&serverAddress, sizeof(serverAddress)) < 0)
	{
		error("SERVER: Error binding port\n");
	}
	
	// Start listening for connetions. Allow up to 5 connections to queue up
  	listen(listenSocket, 5); 

    printf("Server is listening on localhost and port %d\n", portNumber);
    
    // Accept the connection request which creates a connection socket
    connectionSocket = accept(listenSocket, (struct sockaddr *)&clientAddress, &sizeOfClientInfo); 
    if (connectionSocket < 0){
        error("ERROR on accept");
    }

    printf("Client has connected, waiting for response.\nReply with /q to close the program when your turn to chat.\n\n");

    while (1){

        // received client data
        // Clear out the buffer again for reuse
        memset(buffer_client, '\0', sizeof(buffer_client));
        // Read data from the socket, leaving \0 at end
        charsRead = recv(connectionSocket, buffer_client, sizeof(buffer_client) - 1, 0); 
        if (charsRead < 0){
            error("SERVER: ERROR reading from socket");
        }

        // /q was recieved then break and close
        if(strcmp(buffer_client, "/q") == 0){
            break;
        }

        // print what the Client said
        printf("CLIENT (THEM): %s\n", buffer_client); 

        // Get input message from user
        printf("SERVER (YOU): ");
        // Clear out the buffer array
        memset(buffer_server, '\0', sizeof(buffer_server));
        // Get input from the user, trunc to buffer - 1 chars, leaving \0
        fgets(buffer_server, sizeof(buffer_server) - 1, stdin);
        // Remove the trailing \n that fgets adds
        buffer_server[strcspn(buffer_server, "\n")] = '\0'; 

        // Send message to client
        // get chars written
        charsWritten = send(connectionSocket, buffer_server, strlen(buffer_server), 0); 
        if (charsWritten < 0){
            error("SERVER: ERROR writing to socket");
        }
        if (charsWritten < strlen(buffer_server)){
            printf("SERVER: WARNING: Not all data written to socket!\n");
        }

        // if server enters the /q then break and clost
        if(strcmp(buffer_server, "/q") == 0){
            break;
        }
    }
    // close connection socket
    close(connectionSocket); 
    // Close the listening socket
    close(listenSocket); 
    return 0;
}