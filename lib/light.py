import lib.adc as ADC

class LightSensor:
 
    def __init__(self, channel):
        self.channel = channel
        self.adc = ADC.ADC()
 
    @property
    def light(self):
        value = self.adc.read(self.channel)
        return value