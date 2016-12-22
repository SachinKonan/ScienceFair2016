from src.Skonan.ADCCode import ADC
from src.Skonan.DACCode import DAC
import matplotlib.pyplot as plt

if __name__ == '__main__':
    adc = ADC.ADS1x15()
    dac = DAC.MCP4725()

    data = []

    gain = adc.start_adc(0, gain=1)

    increment = 4.096 / 4096
    i = 0
    topV = 2.5

    for x in range(0,2):

        while (i <= topV):
            dac.set_voltage(i)
            data.append([i, adc.get_last_result()])
            i += increment
