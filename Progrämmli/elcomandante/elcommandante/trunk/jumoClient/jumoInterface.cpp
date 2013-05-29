/*
 * jumoInterface.cpp
 *
 *  Created on: 27.02.2012
 *      Author: Felix Bachmair, Konrad Nesteruk
 */

#include "jumoInterface.h"

using namespace std;
jumoInterface::jumoInterface() {
	// TODO Auto-generated constructor stub
	this->printTime();
	isOpen=false;
	isFake=false;
	isLocked =false;
	verbosity=0;
	currentTemp=99;
	currentHum=100;
}

jumoInterface::~jumoInterface() {
	// TODO Auto-generated destructor stub
}
int jumoInterface::printTime(){

   /*time print*/
   t = time(NULL);
   local = localtime(&t);
   if (verbosity)
     printf("\nStart time and date: %s\n", asctime(local));
   return 0;
}


int jumoInterface::convertToInteger(uint16_t data0,uint16_t data1){
	int result = (data0+(data1<<16));
// 	printf("convert to integer: %X %X %d\n", data0,data1,result);
	return result;
}
float jumoInterface::convertToFloat(uint16_t data0,uint16_t data1){
	int value = convertToInteger(data0,data1);
	float result =*((float*)&value);
// 	printf("convert to Float %f\n",result);
	return result;
}


float jumoInterface::analyseOutput(uint16_t data[256],int nWords, float *outputvalue){
	/* data are ok */
	if (verbosity>0)
		fprintf(stderr,"Reader data \n");
	if (verbosity>=0) {
// 		stderr = fopen("temperature.dat", "a");
		local = localtime(&t);
		//fprintf(stderr,"\n%.2i:%.2i:%.2i\t", local->tm_hour, local->tm_min, local->tm_sec);
		printf("%.2i:%.2i:%.2i\t", local->tm_hour, local->tm_min, local->tm_sec);
	}
	for (int i=0;2*i<nWords;i++)
	{
// 		printf("%x+%x<<16",data[i*2],data[i*2+1]);
		float value = convertToFloat(data[i*2],data[i*2+1]);//(data[i*2]+(data[i*2+1]<<16));
		if(i==1){
//			printf("T: %.2f degC\t",value);
			this->currentTemp=value;
		}
		if(i==2){

//			printf("H: %.2f%\t",value);
			//cout<<"\nHum: "<<value<<endl;;
			this->currentHum=value;

		}
		(*outputvalue) = value;
		if (verbosity>0) {
// 			fprintf(stderr,"%.2f\t",*((float*)&data_out[i]));
			printf("%.2f\t",value);
		}
		if (verbosity>1)
			fprintf(stderr,"data %d = %f\n",i+1,value);
		if (verbosity>0)
			fprintf(stderr,"data %d = %.2f\n",i+1,value);
	}
	return 1;//todo
}


int jumoInterface::getValues() {
	printTime();
	for(int u=0;u<256;u++)
			data_out[u]=0;
	int result;
	int address = 0x00a6;
	int length = 6;
	result = read(address,length,&data_out[0]);
 	if (result<0)
	{
		if (result==-1) printf("error : unknown function\n");
		if (result==-2) printf("crc error\n");
		if (result==-3) printf("timeout error\n");
		if (result==-4) printf("error : bad slave answer\n");
	}
	else
	{
		local = localtime(&t);
		if (verbosity) {
			printf("\nStop time and date: %s\n",asctime(local));//,result,data_out);
			for(int k=0;k<6;k++){
				printf("%X\n",data_out[k]);
			}
			printf("\"\n");
		}
	}
	float value;
	result = analyseOutput(data_out,length,&value);
	return result;
}



int jumoInterface::doActions(char action, int program){

	if(verbosity)printf("do %c",action);
	switch (action)
   	{
   		//case 'm': /*printf("")*/;float temp;getValues();return 1;
   		case 'c': cancelProgram();return 1;
   		case 's': programStart();return 1;
   		case 'p': startProgram(program);return 1;
   		case 'l': startLastProgram();return 1;
   		case 'n': nextStep();return 1;
   		case 't': /*printf("")*/;float temp1;getTemperature(&temp1);return 1;
   		case 'h': /*printf("")*/;float hum;getHumidity(&hum);return 1;
	}
	return -1;
}

int jumoInterface::setProgramNumber(int number){
	//option p
	//if(verbosity)
	printf("Set programNo:%d\n",number);
	uint16_t programNo = number;
	return write(0x01B5, programNo);
}
int jumoInterface::instantStart(){
	//if(verbosity)
	printf("Instant Start:\n");
	//option i
	return write(0x01BB,0xFFFF);//Programmstart mit Startzeit in sekunden 0xFFFF= -1 = sofort
}
int jumoInterface::programStart(){
	if(verbosity)printf("Start Program:\n");
	//option s
	//Programmbuffer, Programmstart = 0x1000
	return write(0x01B4, 0x1000);//Programmbuffer,Programmstart
}

int jumoInterface::startProgram(int programNo){
	printf("Start Program no %d:\n",programNo);
	int retVal = setProgramNumber(programNo);
	retVal = instantStart()&&retVal;
	retVal = programStart()&&retVal;
	return retVal;
}

int jumoInterface::getTemperature(float* temp){
	//option t
	//printf("%.2i:%.2i:%.2i\t", local->tm_hour, local->tm_min, local->tm_sec);
	//analyseOutput(char function,uint16_t data[256],int nWords)

	int result =  getValues();
	(*temp)=this->currentTemp;
	return result;

}

int jumoInterface::getHumidity(float* humidity){
	//option h
	int result =  getValues();
	(*humidity)=this->currentHum;
	return result;
}

int jumoInterface::measure(float& temp,float& hum){
	int result =  getValues();
	hum=this->currentHum;
	temp=this->currentTemp;
	return result;
}

int jumoInterface::nextStep(){
	//option n
	//Abschnittswechsel
	if(verbosity)printf("next Step:\n");
	return write(0x0172,0x0004);//Kommando Abschnittswechsel
}


int jumoInterface::startLastProgram(){
	//option l
	//Programmstart des letzten aktivierten Programms
	if(verbosity)printf("Start LastProgram:\n");
	return  write(0x0172,0x1000);//Kommando: ProgrammStart des letzten aktivierten Programms
}

int jumoInterface::closeDevice()
{
//	cout<< "close modbus device: "<<dev<<endl;
	if(!isFake){
		modbus_close(dev);
		modbus_free(dev);
		return 1;
	}
	return 0;
}

int jumoInterface::openDevice()
{
	cout<<"openDevice"<<endl;
	if (isFake)return 0;
	if(verbosity>1)modbus_set_debug(dev, TRUE);
	modbus_set_slave(dev,1);
	cout<<"connectDevice"<<endl;
	int val = modbus_connect(dev);
	cout<<"return of modbus_connect:"<<val<<endl;
    if (val  == -1) {
        fprintf(stderr, "Connection failed: %s\n", modbus_strerror(errno));
        modbus_free(dev);
        isOpen=false;
        isFake=true;
        return -1;
    }
    else
    	isOpen=true;
    return 1;
}

void jumoInterface::setDevice(std::string adresse)
{
	cout<<"setDevice"<<endl;
	if(adresse==""){
		isFake=true;
		cout<<"is Fake Device..."<<endl;
	}
	else {
		isFake=false;
		dev=modbus_new_rtu(adresse.c_str(), 9600, 'N', 8, 1);
		int retVal = openDevice();
		if(retVal<=0) isFake=true;
	}
}

int jumoInterface::cancelProgram(){
	if(verbosity)printf("Cancel Program:\n");
	return write(0x0172,0x0800);//kommando: programmabbruch
}
int jumoInterface::pauseProgram(){
	if(verbosity)printf("Pause Program:\n");
	return write(0x0172,0x2000);//kommando: programhalt
}
int jumoInterface::stopProgram(){
	return cancelProgram();
}
void jumoInterface::setVerbosity(uint16_t verb){
	this->verbosity=verb;
}
//ADDED!!!
int jumoInterface::write(int address,uint32_t value){
	//std::cout<<"write "<<hex<<address<<" "<<hex<<value<<std::endl;
	lock();
	int output;
	if (!isFake)
		output = modbus_write_register(dev,address,value);
		else output = 0;
	unlock();
	return output;
}

int jumoInterface::write(int address,int value){
	//std::cout<<"write "<<hex<<address<<" "<<hex<<value<<std::endl;
	lock();
	int output;
	if (!isFake)
		output = modbus_write_register(dev,address,value);
		else output = 0;
	unlock();
	return output;
}

/**
 * @brief function to calculate dew point out of temperature and relative humidity
 * Formula from http://ag.arizona.edu/azmet/dewpoint.html
 * B = (ln(RH / 100) + ((17.27 * T) / (237.3 + T))) / 17.27
 * D = (237.3 * B) / (1 - B)
 *
 * where:
 *             T = Air Temperature (Dry Bulb) in Centigrade (C) degrees
 *             RH = Relative Humidity in percent (%)
 *             B = intermediate value (no units)
 *             D = Dewpoint in Centigrade (C) degrees
 * @param T Air Temperature in deg C
 * @param RH Relative Humidity in percent
 * @retVal Dew Point in Deg C
 */
float jumoInterface::calculateDewPoint(float T, float RH) {
	float B =(log(RH / 100) + ((17.27 * T) / (237.3 + T))) / 17.27;
	float D = (237.3 * B) / (1 - B);
	return D;
}

int jumoInterface::write(int address,float value){
	if(verbosity)std::cout<<"\n\n\n"<<std::endl;
	if(verbosity)std::cout<<"write float to "<<hex<<address<<" \tval:"<<(float)value<<" "<<std::endl;
	//data
	memcpy(data_out,&value,sizeof(float));
	if(verbosity)cout<<hex<<data_out[0]<<"_"<<hex<<data_out[1]<<"="<<convertToFloat(data_out[0],data_out[1])<<endl;
//	data_out[3]=data_out[1];
//	data_out[1]=data_out[0];
//	data_out[0]=data_out[3];
//	cout<<hex<<data_out[0]<<"_"<<hex<<data_out[1]<<"="<<convertToFloat(data_out[0],data_out[1])<<endl;
	lock();
	int output;
	if (!isFake){
		output = modbus_write_registers(dev,address,2,data_out);
		}
	else output = 0;
	unlock();
	return output;
}


int jumoInterface::read(int address,int length,uint16_t *dest){
	int result;
	if(!isFake){
		lock();
		result = modbus_read_registers(dev,address,length, &data_out[0]);
		unlock();
	}
	else{
		result =0;
		float input[3];
		input[0]=50.5;
		input[1]= 17.0992;
		input[2]= 5.323;
		memcpy(data_out,input,3*sizeof(float));
	}
	return result;
}


int jumoInterface::readSectionNo(int *sectionNo){
	int result;
	int address = 0x011D;
	int length = 4;
	result = read(address,length,&data_out[0]);
////	cout<<"SectionNo: "<<flush;
//	for(int i=0;i<4;i++){
//		int res = data_out[i];
////		cout<<res<<" "<<flush;
//	}
//	cout<<endl;
	int val = data_out[0];
//	cout<<"SectionNo:"<<val<<endl;
	*sectionNo =val;
	return 1;
}

int jumoInterface::readProgramNo(int *programNo){
	int result;
	int address = 0x011C;
	int length = 1;
	result = read(address,length,&data_out[0]);
	int val = data_out[0];
//	cout<<"ProgramNo:"<<val<<endl;
	*programNo = val;
	return result;
}

int jumoInterface::readTargetTemp(float *temp){
	int result;
	int address = 0x00CE;
	int length = 2;
	result = read(address,length,&data_out[0]);
	float val = convertToFloat(data_out[0],data_out[1]);
	*temp = val;
	return true;
}

int jumoInterface::startSection(int sectionNo){
	int lastSection=0;
	readLastSectionNo(&lastSection);
	if(sectionNo>=0&&sectionNo<=lastSection){
		cout<<"start Section "<<sectionNo<<endl;
		int retVal = write(0x01BE,sectionNo);
        	retVal = instantStart()&&retVal;
        	retVal = programStart()&&retVal;

	}
	else
		if(verbosity)cout<<"SectionNo: "<<sectionNo<<" does not fit with lastSection: "<<lastSection<<endl;
	return -1;
}

int jumoInterface::readLastSectionNo(int *lastSectionNo){
	int result;
	int address = 0x0121;
	int length =1;
	result =read(address,length,&data_out[0]);
	int val = data_out[0];
	*lastSectionNo = val;
	return result;
}


int jumoInterface::setTargetTemperature(float temp){
	if(verbosity)cout<<"JumoInterface::setTargetTemp: "<<temp<<endl;
//        int result;
//        int length = 2;
//        result = read(0x00CE,length,&data_out[0]);
//	float t_val = convertToFloat(data_out[0],data_out[1]);
      //  if (t_val != temp) write (0x00CE, temp);
//        return  write (0x00CE,0xBCF5);

	int address = 0x00CE;
	int length = 2;
	read(address,length,&data_out[0]);
	float jumoTargetTemp =convertToFloat(data_out[0],data_out[1]);
	if(temp==jumoTargetTemp)
			return 0;
	if(temp!=jumoTargetTemp)
		cout<<"update TargetTemperature from "<<jumoTargetTemp<<flush;


//
//	length =1;
//	read(address,length,&data_out[0]);
//	cout<<"activate manual mode:"<<hex<<data_out[0]<<endl;
//			//(data_out[0]&0x0200)==0x0200<<endl;;
	address = 0x0172;
	write(address,0x200);
	address = 0x0173;
	write(address,0x0200);//activating manual mode)
//
//	read(address,length,&data_out[0]);
//	cout<<"DONE: "<<hex<<data_out[0]<<endl;

	address = 0x00CE;
	length = 2;
	read(address,length,&data_out[0]);
	float_t newTemp = convertToFloat(data_out[0],data_out[1]);
	if(verbosity)
		cout<<"read TEMP: "<<newTemp<<endl;;
	write(0x00CE,(float)temp);
	write(0x083E,(float)temp); //define setpoint2
	write(0x017A, 2); //change setpoint to setpoint2

	//change to automatic mode
	address = 0x0172;
	write(address,0x0100);
	address = 0x0173;
	write(address,0x0100);
	write(address,0x100);
	write(address,0x0100);

	read(address,length,&data_out[0]);
//	cout<<"read TEMP2: "<<convertToFloat(data_out[0],data_out[1])<<endl;;
	cout<<" to "<< newTemp<<", desired value: "<< temp<<endl;
        // return write(0x0172,0xBCF5);
	return 1;
}

