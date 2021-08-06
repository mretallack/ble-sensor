

import serial
import struct
import uuid

ser = serial.Serial('/dev/ttyACM0', baudrate=115200, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE)  # open serial port



while True:
    
    hexData=None
    try:
        line=ser.readline().decode().rstrip()
        hexData=bytearray.fromhex(line)
    except ValueError:
        pass
    

    while len(hexData) > 0:
        
        hexString="".join("%02x" % b for b in hexData)
    
    
        NumberOfBytes=hexData[0]
        
        TypeOfEntry=hexData[1]
        
        if TypeOfEntry == 0x01:
            # flags type
            FlagsValue=hexData[2]
            #   bit 0 (OFF) LE Limited Discoverable Mode
            #   bit 1 (OFF) LE General Discoverable Mode
            #   bit 2 (ON) BR/EDR Not Supported
            #   bit 3 (OFF) Simultaneous LE and BR/EDR to Same Device Capable (controller)
            #   bit 4 (OFF) Simultaneous LE and BR/EDR to Same Device Capable (Host)
            #print("Flags: "+str(FlagsValue))
            
        elif TypeOfEntry == 0x03:
        
            # Complete List of 16-bit Service Class UUIDs
            service=hexData[2:3]
            
            #print("service: "+str(service))
            
        elif TypeOfEntry == 0x09:
            # Complete Local Name AD Type
            nameLength = NumberOfBytes-1
            
            CompleteLocalNameAD= hexData[2:nameLength].decode("utf-8")
            
            #print("CompleteLocalNameAD: "+CompleteLocalNameAD)

        elif TypeOfEntry == 0xFF:
        
            # Manufacturer specific data AD type
            
            # Company identifier code
            CompanyIdentifierCode="".join("%02x" % b for b in hexData[2:4])
            
            print(CompanyIdentifierCode)
            
            # 
            # 00050001-0000-1000-8000-00805f9b0131              
            
            # 25     xx*     Major 1st byte     set major value
            # 26     xx*     Major 2nd byte     set major value
            # 27     xx*     Minor 1st byte     set minor value
            # 28     xx*     Minor 2nd byte     set minor value
            # 29     0xb3    Signal power (calibrated RSSI@1m)     signal power value
            
            print(hexString)
            
            if NumberOfBytes > 20:
                
                print(hexData[22])
                major=hexData[22]<<8 | hexData[23]
                
                minor=hexData[24]<<8 | hexData[25]
                
                print("major: "+str(major))
                print("minor: "+str(minor))
                
                uuid_code=uuid.UUID("".join("%02x" % b for b in hexData[6:6+16]))
    
                print(uuid_code)
                
                if uuid_code == uuid.UUID("00050001-0000-1000-8000-00805f9b0131"):
                    
                    print("Cypress Device detected")
                    
                    temperature=175.72*((minor & 0xff)*256)/65536 - 46.85
                    humidity=125.0*(minor & 0xff00)/65536 - 6
                    
                    print("Temperature: "+str(temperature))
                    print("Humidity: "+str(humidity))
                

        hexData=hexData[NumberOfBytes+1:]
    
    #09 # Complete Local Name AD Type
    #38 42 42 41 43 34 39 44 # "8BBAC49D"
    #07 # Number of bytes that follow in the second AD Structure
    #16 # Service Data AD Type
    #09 18 # 16-bit Service UUID 0x1809 = Health thermometer (org.bluetooth.service.health_thermometer)
    #44 08 00 FE # Additional Service Data 440800  (Temperature = 0x000844 x 10^-2) = 21.16 degrees
    #04 # Number of bytes that follow in the third AD Structure
    #16 # Service Data AD Type
    #0F 18 # 16-bit Service UUID 0x180F  = Battery Service (org.bluetooth.service.battery_service) 
    #5B # Additional Service Data (battery level)
    #B2 # checksum
    
    
    
    
    #hexString="".join("%02x" % b for b in hexData)
    
    
    #if "020106090951484d2d46343330" != hexString:
    #    print(hexString)        

        
        


ser.close()             # close port

