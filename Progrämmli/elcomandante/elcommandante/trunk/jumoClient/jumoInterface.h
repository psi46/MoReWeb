/*
 * jumoInterface.h
 *
 *  Created on: 27.02.2012
 *      Author: Felix Bachmair
 */

#ifndef JUMOINTERFACE_H_
#define JUMOINTERFACE_H_

#include <stdio.h>
#include <stdint.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>
#include <errno.h>
#include <modbus.h>
#include <modbus/modbus.h>
#include <time.h>
#include <string>
#include <ostream>
#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>


class jumoInterface {
public:
	jumoInterface();
	virtual ~jumoInterface();
	void setDevice(std::string adresse="/dev/ttyD0");
	int doActions(char action, int program);
	void setVerbosity(uint16_t verb);
private:
	int openDevice();
	int closeDevice();
	int convertToInteger(uint16_t data0,uint16_t data1);
	float convertToFloat(uint16_t data0,uint16_t data1);
	int getValues();
	float analyseOutput(uint16_t data[256],int nWords, float *outputvalue);
public:
	int measure(float &temp,float &hum);
	int printTime();
	int setProgramNumber(int number);
	int instantStart();
	int programStart();
	int startProgram(int programNo);
	int getTemperature(float* temp);
	int getHumidity(float* humidity);
	int nextStep();
	int startLastProgram();
	int cancelProgram();
	int pauseProgram();
	int stopProgram();
	int readSectionNo(int *sectionNo);
	int readProgramNo(int *programNo);
	int readTargetTemp(float *temp);
	int readLastSectionNo(int *lastSectionNo);
	int startSection(int sectionNo);
	int setTargetTemperature(float temp);
	float calculateDewPoint(float temp, float relHum);
private:
	int read(int address,int length,uint16_t *dest);
	int write(int address,uint32_t value);
        int write(int address,int value);
	int write(int address,float value);
	void lock(){while (isLocked)usleep(50);isLocked=true;}
	void unlock(){usleep(50);isLocked=false;};
	bool isLocked;
	float currentTemp;
	float currentHum;
	modbus_t *dev;
	struct tm *local;
	time_t t;
	uint16_t verbosity;

	int data_in[256];
	//   uint8_t data_out[256];
	uint16_t data_out[256];
	bool isOpen;
	bool isFake;
};

#endif /* JUMOINTERFACE_H_ */
