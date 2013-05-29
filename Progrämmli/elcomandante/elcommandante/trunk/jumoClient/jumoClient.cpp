//============================================================================
// Name        : jumoClient.cpp
// Author      : 
// Version     :
// Copyright   : Your copyright notice
// Description : Hello World in C, Ansi-style
//============================================================================
#include <sys/select.h>
#include <errno.h>
#include <unistd.h>	// read, STD*_FILENO
#include <stdio.h>
#include <stdlib.h>
#include <string>
#include "jumoInterface.h"
#include "jumoSubClientHandler.h"
#include <subsystem/subClientHandler.h>
#include "error.h"
#include "subsystem/error.h"
#include "subsystem/signalnames.h"
#include <signal.h>	// signal()
#include <pthread.h>
//void print_sum(float x, float y)
//{
//  std::cout << "The sum is " << x+y << std::endl;
//}

using namespace std;
jumoSubClientHandler *client;

std::string address= "/dev/F0";
bool verbosity=false;
bool isFakeDevice;
void cleanexit() {
	eprintf("clean exit\n");
	client->CloseClient();
	sleep(1.0);
	client->killClient();
//	client.closeConnection();
	std::cout<<"client: "<<client->isOk()<<std::endl;
//	wantexit = 1;
}


void sigint_handler(int sig) {
	client->killClient();
	eprintf("received %s(%d)\n", SIGNAME[sig], sig);
	client->killClient();

	client->closeConnection();
	std::cout<<"client: "<<client->isOk()<<std::endl;
}

void printHelp(){
    cout<<"Help for Jumo Client:"<<endl;
    cout<<"\t-d\tSet device address, e.g. /dev/ttyF0, default /dev/F0"<<endl;
    cout<<"\t-f\tWork as a fake client"<<endl;
    cout<<"\t-v\tVerbose mode"<<endl;
    cout<<"\t-h\tShow this help meassge"<<endl;
}

bool readInputs(int argc,char ** argv){
	isFakeDevice = false;
	for(int i=1; i < argc; i++)
	{
		if(std::string(argv[i]) == "-h"||std::string(argv[i])=="--help")
		{
			printHelp();
			exit(0);
		}
		else if(std::string(argv[i]) == "-d")
		{
			i++;
			address = std::string(argv[i]);
			std::cout<<"Setting device Address = "<<address<<std::endl;
		}
		else if(std::string(argv[i]) == "-f")
		{
			isFakeDevice=true;
			std::cout<<"Test Program with faked jumo device"<<std::endl;
		}
		else if(std::string(argv[i]) == "-v")
		{
			verbosity=true;
			std::cout<<"Start program with verbose level"<<std::endl;
		}
	}
	if(isFakeDevice)
		address="";
	return true;
}

int main(int argc, char *argv[]) {
	readInputs(argc,argv);
	client = new jumoSubClientHandler("jumoClient",address);
	client->setVerbosity(verbosity);
	atexit(cleanexit);
	signal(SIGINT, sigint_handler);
	signal(SIGTERM, sigint_handler);
//	jumoInterface jumo;
//	boost::signal<void (float, float)> sig;
//
//	sig.connect(&print_sum);
//	sig(5, 3);
//	int program   = -1;
//	int verbosity=0;
	client->subscribeAbo("/jumo");
	client->getAboFromServer();
	client->setTimeOut(2);
	//pthread_t p1;
	client->sendAndReceive();
//	pthread_create (&p1, NULL,client.receiveAbos, NULL);
//	int i = 0;
//	for ( i = 0; i < argc; ++i) {
//		if (!strcmp(argv[i],"-c"))  {i++;
//		sprintf(whichAction,"c",argv[i]); }
//		//actionto perform on jumo
//		if (!strcmp(argv[i],"-p"))  {program    = atoi(argv[++i]); sprintf(whichAction,"p");}
//		//program number 0 - 49 --> 1 - 50
//		if (!strcmp(argv[i],"-v"))  {verbosity=atoi(argv[++i]);jumo.setVerbosity(verbosity); }
//		// verbosity 0,1,2
//	}
//	//if(program != -1) whichAction = "p)
//	if(verbosity)printf("Action %s\n",whichAction);
//	if(verbosity)printf("Program %d\n",program);
//
//	/* open device */
//	int device;
//	jumo.setDevice("");
//	if(verbosity)printf("now trying to start program...");
//	jumo.doActions(whichAction[0],program);
	client->killClient();
	client->closeConnection();
	while(!client->isClientKilled())
		usleep(10);
	delete client;
	return EXIT_SUCCESS;
}
