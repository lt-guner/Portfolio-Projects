// Class: C344
// Term: Winter 2022
// Assignment: Project 3
// Author: Timur Guner

#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <sys/wait.h>
#include <sys/types.h>
#include <unistd.h>
#include <signal.h>
#include <fcntl.h>

#define max_length 2048
#define max_args 512
#define process_amount 512

//global to be used in handlers;
int processstatus;
int foregroundstage;
int processtracker[process_amount];

void handle_SIGTSTP(int signo){
    // if the foregroundstage is 0, it means the the foreground process needs to be turned on
    // let the user know they are entering foreground mode and set the foregroundstage to 1
    if (foregroundstage == 0)
    {
        char* message = "\nEntering foreground-only mode (& is now ignored)\n: ";
        write(STDOUT_FILENO, message, 52);
        foregroundstage = 1;
    }
    // do the reverse if SIGTSTP is triggered again
    else
    {
        char* message = "\nExiting foreground-only mode\n: ";
        write(STDOUT_FILENO, message, 32);
        foregroundstage = 0;
    }
}

int main(){

    for (int i; i < process_amount; i++){
		processtracker[i] = 0;
	}

    // this processcount is used to keep track of any process ids that need to be checked
    int processcount = 0;

    // initialize the tracking of foreground switching
    foregroundstage = 0;

	// the while loop that continues the shell until complete
    while(1)
    {
        // flush everything standard
        fflush(stdout);
        fflush(stdin);
        fflush(stderr);

		// foreground process to deal with the printing out background signals running
		for (int i = 0; i < process_amount; i++)
		{
			// look for background processes that were saved
			if (processtracker[i] != 0){
				
				// declare a status variable
				int childexitstatus;
				// pull the status of the child and a updated pid
				int childpidupdate = waitpid(processtracker[i], &childexitstatus, WNOHANG);
				// if processes were 0 or 1, then success
                if ((childexitstatus == 0 || childexitstatus == 1) && childpidupdate != 0) {
                    fprintf(stdout,"Background pid %d is done: exit value %d\n",childpidupdate,childexitstatus);
					processtracker[i] = 0;
                }
                // else print that is was terminated by a signal
                else if (childpidupdate != 0) {
					fprintf(stdout,"Background pid %d is done: terminated by signal %d\n",childpidupdate,childexitstatus);
					processtracker[i] = 0;
                }
			}
		}

        // custom signalers
        // set the sigint to ignore at the moment and can only work if the the process is running in the foreground and if we are in background mode
        struct sigaction SIGINT_action = {0};
        SIGINT_action.sa_handler = SIG_IGN;
        sigfillset(&SIGINT_action.sa_mask);
        SIGINT_action.sa_flags = 0;
        sigaction(SIGINT, &SIGINT_action, NULL);

        // custom sigtstp to be ignored at the moment
        struct sigaction SIGTSTP_action = {0};
        SIGTSTP_action.sa_handler = handle_SIGTSTP;
        sigfillset(&SIGTSTP_action.sa_mask);
        SIGTSTP_action.sa_flags = SA_RESTART;
        sigaction(SIGTSTP, &SIGTSTP_action, NULL);
        

        // create a list of arguments to store the max number of arguments
        // create a pointer called commandenter to for getline
        // and have a variable to keep track of the number of arguments
        // an array that will be used for input expansion
        // a bufsize for the getline
        char *argumentlist[max_args];
        char *commandenter;
        int numberofargs = 0;
        char inputforexanpsion[max_length];
        size_t bufsize = 0;
        
        // declate the necessary variables for the child processes and statuts
        pid_t childpid = -5;
	    
        int backgroundamp = 0; // if statement ends in &

        // For use with strtok_r to keep track of the current arguement and the pointer
        char *saveptr;
        char *currarg = NULL;

        // redirect flag if > or < are in the arguments and an 
        int redirect;
        int redirectin;
        int redirectout;
        int fd;

        // write the prompt to for input and flush then used getline to store standard in and removed the newline
        printf(": ");
        fflush(stdout);
        getline(&commandenter, &bufsize, stdin);
        strtok(commandenter, "\n");

        // the for loop will iterate through the commandenter and do $$ expansion by replacing the $$ with %d
        for(int i = 0; i< strlen (commandenter); i++) 
        {
            if(commandenter[i] == '$' && commandenter[i+1] == '$') 
            {
                commandenter[i] = '%';
                commandenter[i+1] = 'd';
            }
        }

        // the output needs to be stored in a new array using sprintf
        sprintf(inputforexanpsion, commandenter, getpid());
        
        // user the token method to loop through the commange and store the individual arguments in an array
        char *token = strtok(inputforexanpsion, " ");
        while(token != NULL) 
        {
            argumentlist[numberofargs] = token;
            numberofargs++;
            token = strtok(NULL, " ");
        }

        // The index after the last filled index will be NULL for the exec function
        argumentlist[numberofargs] = NULL;
        fflush(stdout);
    
        // skip if number of argumenrs is 0 because it was all spaces
        if (numberofargs == 0)
        {
            continue;
        }
        // else move on to checking the ampersand for background
        else if (strcmp(argumentlist[numberofargs-1],"&") == 0)
        {
            backgroundamp = 1;
            argumentlist[numberofargs-1] = NULL;
        }


        // handle the entered key by user with no command
        if (strcmp(argumentlist[0], "\n") == 0)
        {
            continue;
        }
        // else exit the program if the command command exit is entered reguardless if other entries are present
        else if (strcmp(argumentlist[0], "exit") == 0)
        {	
            // loop through the tracked processed and kill ones that exist
			for(int i=0;i < process_amount; i++)
	        {
                if (processtracker[i] != 0){
                    kill(processtracker[i], SIGKILL);
                }
	        }	
            // exit when complete
			exit(0);
        }
        // else built in cd feature in which the user goes to the home directory or changes directory using the cd
        else if (strcmp(argumentlist[0], "cd") == 0){
            if (numberofargs == 1){
                chdir(getenv("HOME"));
            }
            else{
                chdir(argumentlist[1]);
            }
        }
        // else ignore anthing that starts with with #
        else if (strcmp(argumentlist[0], "#") == 0)
        {
            continue;
        }
        // reports the status if the user used the status update
		else if (strcmp(argumentlist[0], "status") == 0)
        {
			if (WIFEXITED(processstatus))
            {
				printf("exit value %d\n", WEXITSTATUS(processstatus));
			}
			else if (WIFSIGNALED(processstatus))
            {
				printf("terminated by signal %d\n", WTERMSIG(processstatus));
			}
		}
        // other other processes fork into the else statement
        else{

            // fork
            fflush(stdout);
            childpid = fork();
            
            // switch to fork the child
            switch(childpid)
            {
                case -1:
                    // if failed
                    perror("fork() failed!");
                    fflush(stdout);
                    fflush(stderr);
                    exit(1);
                    break;
                case 0:

                    // do the following if there is no background command
                    //if (backgroundamp == 0)
                    
                    
                    // do the following if there is a background command in non-foreground mode, because foreground doesnt process background commands
                    // its the same but we control the standard input and output to /dev/null if redirections are not specified
                    if (backgroundamp == 1 && foregroundstage == 0)
                    {
                        // we must loop through the array start at index one to see if there are redirects
                        for(int i = 1; i < numberofargs; i++)
                        { 
                            // This prevents any error raised in NULL
                            if (argumentlist[i] != NULL){
                                // open the source file for read only
                                // adopted from https://canvas.oregonstate.edu/courses/1884946/pages/exploration-processes-and-i-slash-o?module_item_id=21835982
                                if (strcmp(argumentlist[i],"<") == 0)
                                {
                                    redirect = 1;
                                    fd = open(argumentlist[i+1], O_RDONLY);
                                    int result = dup2(fd, STDIN_FILENO);
                                    if (fd == -1) 
                                    { 
                                        printf("cannot open %s for input\n", argumentlist[i+1]);
                                        fflush(stdout);
                                        exit(1); 
                                    }
                                    redirectin = 1;
                                }
                                // open the target file fior write
                                // adopted from https://canvas.oregonstate.edu/courses/1884946/pages/exploration-processes-and-i-slash-o?module_item_id=21835982
                                if (strcmp(argumentlist[i],">") == 0)
                                {
                                    redirect = 1;
                                    fd = open(argumentlist[i+1], O_WRONLY | O_CREAT | O_TRUNC, 0644);
                                    int result = dup2(fd, STDOUT_FILENO);
                                    if (fd == -1) 
                                    { 
                                        printf("cannot open %s for output\n", argumentlist[i+1]);
                                        fflush(stdout);
                                        exit(1);
                                    }
                                    redirectout=1;
                                }
                            }
                        }

                        // if a redirect was not specified then we send the process to /dev/null
                        if (redirectin != 1)
                        {
                            fd = open("/dev/null",O_RDONLY);
                            dup2(fd, STDIN_FILENO);
                        }
                        if (redirectout != 1)
                        {
                            fd = open("/dev/null",O_WRONLY);
                            dup2(fd, STDOUT_FILENO);
                        }
                          
                    }
                    // do the following if there is no background command
                    else
                    {
                        // we must loop through the array start at index one to see if there are redirects
                        for(int i = 1; i < numberofargs; i++)
                        { 
                            // This prevents any error raised in NULL
                            if (argumentlist[i] != NULL){
                                // open the source file for read only
                                // adopted from https://canvas.oregonstate.edu/courses/1884946/pages/exploration-processes-and-i-slash-o?module_item_id=21835982
                                if (strcmp(argumentlist[i],"<") == 0)
                                {
                                    redirect = 1;
                                    fd = open(argumentlist[i+1], O_RDONLY);
                                    int result = dup2(fd, STDIN_FILENO);
                                    if (fd == -1) 
                                    { 
                                        printf("cannot open %s for input\n", argumentlist[i+1]);
                                        fflush(stdout);
                                        exit(1); 
                                    }
                                }
                                // open the target file fior write
                                // adopted from https://canvas.oregonstate.edu/courses/1884946/pages/exploration-processes-and-i-slash-o?module_item_id=21835982
                                if (strcmp(argumentlist[i],">") == 0)
                                {
                                    redirect = 1;
                                    fd = open(argumentlist[i+1], O_WRONLY | O_CREAT | O_TRUNC, 0644);
                                    int result = dup2(fd, STDOUT_FILENO);
                                    if (fd == -1) 
                                    { 
                                        printf("cannot open %s for output\n", argumentlist[i+1]);
                                        fflush(stdout);
                                        exit(1);
                                    }
                                }  
                            }
                        }
                    }

                    // if there were redirects those need to be eliminated from the argumentlist
                    // we already handling the reading and writing and those special characters cannot go to the excevp
                    // again start at index where the first file would be located
                    if (redirect == 1)
                    {
                        for (int i = 1; i < numberofargs; i++){
                            argumentlist[i] = NULL;
                        }
                        close(fd);
                    }

                    if((backgroundamp == 0 && foregroundstage == 0)||(backgroundamp == 0 && foregroundstage == 1)||(backgroundamp == 1 && foregroundstage == 1)){
                        // custom signal handler allows for the user to kill a foreground process if there are in background mode
                        struct sigaction SIGINT_action = {0};
                        SIGINT_action.sa_handler = SIG_DFL;
                        sigfillset(&SIGINT_action.sa_mask);
                        SIGINT_action.sa_flags = 0;
                        sigaction(SIGINT, &SIGINT_action, NULL);
                    }

                    // send the command list to the output using excevp as recommended by the the assignment instructions
                    if (execvp(argumentlist[0], argumentlist)==-1) {
                        printf("%s: no such file or directory\n", argumentlist[0]);
                        fflush(stdout);
                        exit(1);
			        }

                default:

                    // if not in the foreground process and an ampersand was triggered background to run then do this
                    if(backgroundamp == 1 && foregroundstage == 0)
                    {
                        // print the child process to the user, flush, reset background, and increment the process count
                        printf("background pid is %d\n", childpid);
                        fflush(stdout);
                        backgroundamp = 0;
                        //processcount++;

						// add the background process to the process tracker
						for (int i; i < process_amount; i++){
							if (processtracker[i] == 0)
							{
								processtracker[i] = childpid;
								break;
							}
						}
                    }
                    //else every other combo goes here
                    else
                    {
                        // the waitpid for the child process and flush if the sigint was called
                        waitpid(childpid, &processstatus, 0);
                        fflush(stdout);

                        // if the process signal was terminated then let the user now
                        if (WIFSIGNALED(processstatus) == 1 && WTERMSIG(processstatus) != 0){
								printf("terminated by signal %d\n", WTERMSIG(processstatus));
                                fflush(stdout);
							}
                    }
                    break;
            }
        }
    }
    return 0;
}