from enum import IntEnum
from switch import switch
import serial
from mesh.generic.customExceptions import NoSerialConnection

class RadioMode(IntEnum):
    off = 0
    sleep = 1
    receive = 2
    transmit = 3

class Radio(object):

    def __init__(self, serial, config):
        self.serial = serial
        self.mode = RadioMode.off
        
        # Read
        self.uartNumBytesToRead = config['uartNumBytesToRead']
        self.rxBufferSize = config['rxBufferSize']
        self.clearRxBuffer()

        # Send
        self.txBuffer = bytearray()
    
    def setMode(self, mode):
        """Change radio operating mode (i.e. rx, tx, sleep, off)."""
        if mode != self.mode:
            for case in switch(mode):
                if case(RadioMode.off):
                    self.setOff()
                    break
                if case(RadioMode.sleep):
                    self.setSleep()
                    break
                if case(RadioMode.receive):
                    self.setReceive()
                    break
                if case(RadioMode.transmit):
                    self.setTransmit()
                    break

    def setSleep(self):
        self.mode = RadioMode.sleep

    def setOff(self):
        self.mode = RadioMode.off

    def setReceive(self):
        self.mode = RadioMode.receive

    def setTransmit(self):
        self.mode = RadioMode.transmit

    # Read methods
    def clearRxBuffer(self):
        """Reset receive buffer."""
        self.rxBuffer = bytearray(self.rxBufferSize)
        self.bytesInRxBuffer = 0

    def readBytes(self, bufferFlag):
        """Reads raw bytes from serial connection"""
        if not self.serial:
            raise NoSerialConnection("No serial connection available")
            return 0 
        
        # Read from serial port
        newBytes = []
        try:
            newBytes = self.serial.read(self.uartNumBytesToRead)
        except serial.SerialException:
            return 0

        # Process rx bytes
        if newBytes:
            self.processRxBytes(newBytes, bufferFlag)

        return len(newBytes)

    def processRxBytes(self, newBytes, bufferFlag):
        """Default behavior just adds directly to rxBuffer."""
        self.bufferRxMsg(newBytes, bufferFlag)

    def bufferRxMsg(self, newBytes, bufferFlag):
        # Put read bytes in buffer
        if not newBytes:
            return

        numNewBytes = len(newBytes)    
        if bufferFlag == True: # Add new bytes read to buffer
            if (self.bytesInRxBuffer + numNewBytes) <= len(self.rxBuffer): # Prevent rx buffer overload  
                self.rxBuffer[self.bytesInRxBuffer:self.bytesInRxBuffer+numNewBytes] = newBytes
                self.bytesInRxBuffer += numNewBytes
            else:
                print("Warning: Radio buffer rx overflow.")
        else: # Replace buffer contents with new bytes
            self.rxBuffer[0:numNewBytes] = newBytes
            self.bytesInRxBuffer = numNewBytes

    def getRxBytes(self):
        return self.rxBuffer[0:self.bytesInRxBuffer]

    # Send methods
    def sendBytes(self, msgBytes):
        """Sends bytes provided bytes directly out over serial connection.  This method provides no bandwidth usage control."""
        if not self.serial:
            raise NoSerialConnection("No serial connection available")
            return 0  
        
        try:
            return self.serial.write(msgBytes)
            
        except serial.SerialException:
            pass
            
    def sendMsg(self, msgBytes):
        """Packages provided bytes into properly formatted message for radio and transmits.  This method provides no bandwidth usage control."""

        bytesSent = 0
        if len(msgBytes) > 0:
            msg = self.createMsg(msgBytes)
            bytesSent = self.sendBytes(msg)

        return bytesSent

    def bufferTxMsg(self, msgBytes):
        self.txBuffer += msgBytes

    def createMsg(self, msgBytes):
        """Default behavior is to just pass through raw bytes."""
        return msgBytes

    def sendBuffer(self, maxBytesToSend=0):
        """This is the primary method for transmitting bytes using the Radio.  This method allows the radio to regulate how much data is being sent out."""
        bytesSent = 0

        if self.txBuffer:
            if maxBytesToSend > 0 and len(self.txBuffer) > maxBytesToSend: # too much data to send
                bytesSent = self.sendMsg(self.txBuffer[:maxBytesToSend])
                self.txBuffer = self.txBuffer[maxBytesToSend:] # remove sent bytes from buffer
            else: # send entire buffer
                bytesSent = self.sendMsg(self.txBuffer)
            
                # Clear tx buffer
                self.txBuffer = bytearray()

        return bytesSent

    def sendCommand(self, cmd):
        """Issue command to radio."""
        pass
