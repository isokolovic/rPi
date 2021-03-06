import RPi.GPIO as GPIO
import time

def bin2dec(string_num):
    return str(int(string_num, 2))

def DHT_data():    
    data = []
    humidity_temp = []

    GPIO.setmode(GPIO.BCM)

    GPIO.setup(4, GPIO.OUT)
    GPIO.output(4, GPIO.HIGH)
    time.sleep(0.025)
    GPIO.output(4, GPIO.LOW)
    time.sleep(0.02)

    GPIO.setup(4, GPIO.IN, pull_up_down = GPIO.PUD_UP)

    for i in range(0, 1):
        data.append(GPIO.input(4))

    bit_count = 0
    tmp = 0
    count = 0
    HumidityBit = ""
    TemperatureBit = ""
    crc = ""

    try:
        while data[count] == 1:
            tmp = 1
            count += 1

        for i in range(0, 32):
            bit_count = 0

            while data[count] == 0:
                tmp = 1
                count += 1

            while data[count] == 1:
                bit_count += 1
                count += 1

            if(bit_count > 3):
                if(i >= 0 and i < 8):
                    HumidityBit += "1"
                
                if(i >= 16 and i < 24):
                    TemperatureBit += "1"

            else:
                if(i >= 0 and i < 8):
                    HumidityBit += "0"
                
                if(i >= 16 and i < 24):
                    TemperatureBit += "0"

    except:
        print("ERR_RANGE")
        exit(0)

    Humidity = bin2dec(HumidityBit)
    Temperature = bit2dec(TemperatureBit)

    if ((int(Humidity) + int(Temperature) - int(bin2dec(crc))) == 0):
        # print("Humidity: " + Humidity + "%")
        # print("Temperature: " + Temperature + "C")
        humidity_temp.append(Temperature)
        humidity_temp.append(Humidity)
        return humidity_temp
    
    else:
        # print("ERR_CRC")
        return("ERR_CRC")

if __name__ == '__main__':
    DHT_data()