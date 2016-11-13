from ADC import ADCThread

if __name__ == "__main__":
	# path: /home/pi/Documents/PythonProjects/ScienceFair2016/ADC
	#run: python simptest.py
	adc = ADCThread(address= 0x48, gain = 2/3)
	adc.start()
	
	while True:
		print('%d , %d , %d , %d ' % (adc.getADCVal1(),adc.getADCVal2(),adc.getADCVal3(),adc.getADCVal4()))
