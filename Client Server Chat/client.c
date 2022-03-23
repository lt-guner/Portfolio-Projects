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
	
	// exit if incorrect arguments
    if (argc != 2)
    {
        error("USAGE: ./client port#\n");
    }

    // variables needed to connected to server
    int socketFD, portNumber, charsRead, charsWritten;
    struct sockaddr_in serverAddress;
    struct hostent* hostInfo;
    char buffer_server[1024];
    char buffer_client[1024];

	// Clear out the address struct
    memset((char*)&serverAddress, '\0', sizeof(serverAddress));
    
    // The address should be network capable
    serverAddress.sin_family = AF_INET;
    
    // Store the port number
    portNumber = atoi(argv[1]);
    serverAddress.sin_port = htons(portNumber);

	// Get the DNS entry for this host name and exit if it doesnt exist
    hostInfo = gethostbyname("localhost"); 
    if (hostInfo == NULL) 
    {
        error("CLIENT: Error no such host\n");
    }

	// Copy the first IP address from the DNS entry to sin_addr.s_addr
    memcpy((char*)&serverAddress.sin_addr.s_addr, (char*)hostInfo->h_addr, hostInfo->h_length);

    // Create a socket and print to stderr if fails
    socketFD = socket(AF_INET, SOCK_STREAM, 0); 
    if (socketFD < 0)
    {
        error("CLIENT: Error opening socket\n");
    }

	// Connect to server and return failure if not connected
    if (connect(socketFD, (struct sockaddr*)&serverAddress, sizeof(serverAddress)) < 0)
    {
        error("CLIENT: Error connecting\n");
    }

    printf("Client has conntected to localhost and port %d\n", portNumber);
    printf("Enter a message to send to start chat.\nReply with /q to close the program when your turn to chat.\n\n");

    while (1){
        // Get input message from user
        printf("CLIENT (YOU): ");
        // Clear out the buffer array
        memset(buffer_client, '\0', sizeof(buffer_client));
        // Get input from the user, trunc to buffer - 1 chars, leaving \0
        fgets(buffer_client, sizeof(buffer_client) - 1, stdin);
        // Remove the trailing \n that fgets adds
        buffer_client[strcspn(buffer_client, "\n")] = '\0'; 

        // Send message to server
        // get chars written
        charsWritten = send(socketFD, buffer_client, strlen(buffer_client), 0); 
        if (charsWritten < 0){
            error("CLIENT: ERROR writing to socket");
        }
        if (charsWritten < strlen(buffer_client)){
            printf("CLIENT: WARNING: Not all data written to socket!\n");
        }

        // if entered /q then break and clost
        if(strcmp(buffer_client, "/q") == 0){
            break;
        }

        // Get return message from server
        // Clear out the buffer again for reuse
        memset(buffer_server, '\0', sizeof(buffer_server));
        // Read data from the socket, leaving \0 at end
        charsRead = recv(socketFD, buffer_server, sizeof(buffer_server) - 1, 0); 
        if (charsRead < 0){
            error("CLIENT: ERROR reading from socket");
        }

        // if /q was received then break and close
        if(strcmp(buffer_server, "/q") == 0){
            break;
        }

        // print the message received if not /q
        printf("SERVER (THEM): %s\n", buffer_server);    
    }

    // Close the socket
    close(socketFD);  
    return 0;
}