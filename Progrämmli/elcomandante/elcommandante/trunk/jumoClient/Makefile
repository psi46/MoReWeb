
LLABCPPFLAGS  	:= -I/usr/local/include
LLABCPPFLAGS	+= -I$(HOME)/lib/subsystem -I/usr/local/include/modbus -I$(HOME)/lib

LLABLDFLAGS		:= -I/usr/local/include
LLABLDFLAGS		+= -L$(HOME)/lib/ -lsubsystem

ROOTCFLAGS		:= $(shell root-config --cflags)
ROOTLIBS		:= $(shell root-config --libs)
ROOTGLIBS   	:= $(shell root-config --glibs)
LDFLAGS	      	:= -g $(LLABLDFLAGS) $(ROOTLIBS)
SOFLAGS       	:= -shared

CPP         	:= g++
CPPFLAGS    	:= -O -Wall -fPIC -I..\
					$(LLABCPPFLAGS) $(ROOTCFLAGS)

CXXFLAGS =	-O2 -g -Wall -fmessage-length=0 -I$(HOME)/sdvlp/libmodbus-3.0.3/src -I/home/veloxid/lib $(CPPFLAGS)

OBJS =		jumoClient.o jumoInterface.o scpiInterpreter.o jumoSubClientHandler.o

LIBS = -lmodbus   $(LLABLDFLAGS) -L../subsystem

TARGET =	jumoClient

$(TARGET):	$(OBJS)
	$(CPP) -o $(TARGET) $(OBJS) $(LIBS)

all:	$(TARGET)

clean:
	rm -f $(OBJS) $(TARGET)
