import lib
import time

def main():
	
	lcd = lib.lcd.JHD1802()

	dht11 = lib.dht.DHT("11",16)

	light = lib.light.LightSensor(0)
	
	while (True):
		humi,temp = dht11.read()

		text0 = "T="
		text0 += str(temp)
		text0 += "C H="
		text0 += str(humi) 
		text0 += "%"

		text1 = "L="
		text1 += str(light.light)

		lcd.clear()
		lcd.setCursor(0, 0)
		lcd.write(text0)
		lcd.setCursor(1, 0)
		lcd.write(text1)

		time.sleep(1)

if __name__=='__main__':
	main()