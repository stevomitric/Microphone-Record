info = '''
          __ ___________            
  _______/  |\_   _____/__  ______  
 /  ___/\   __\    __)_\  \/ /  _ \ 
 \___ \  |  | |        \\    (  <_> )
/____  > |__|/_______  / \_/ \____/ 
     \/              \/             
	 
'''
usage = '''
Created by stEvo (stevo.mitric@yahoo.com)

Usage:
	sound_record [options]
	
	--rate NUM		- sets recording rate (default: 10000)
	--format NUM		- available: (8 (default), 4, 2)
	--chunk	NUM		- Chunk size to read (default: 1024)
	--saveto PATH		- Saves the recording in a file
	--recordfor NUM		- Records for NUM seconds
	--noautosave		- Saves into file after recording is done
	--livefeedback		- Plays audio direcly from microphone
	--readfromfile FILE	- Reads requests from file
	--help			- Displays this info and quits
	
	
	Examples:
		sound_record --rate 40000 --saveto "test.wav" --recordfor 10
		sound_record --saveto "test.wav" --recordfor 20 --livefeedback
		sound_record --readfromfile "C:\programdata\file.txt"
	
	File from "readfromfile" argument, you must define as follows:
	
	time: 1504037551
	rate: 10000
	format: 8
	chunk: 1024
	saveto: "/programdata/sound.wav"
	createwavafterfinish: 0
	
	Time is an argument that defines when the program will stop. You can
	get the value by calling time.time() in python (2.7.11)
	Program will loop as long as you defined all the arguments correcly and
	as long as the file exists in [FILE] path.
	
'''

import pyaudio, wave, time, sys, os

from threading		import Thread

class Main:
	def __init__(self):
		
		self.settings = {
			'rate': 10000,
			'format': 8,
			'chunk': 1024,
			'saveto': 'test.wav',
			'recordfor': 0,
			'noautosave': 0,
			'livefeedback': 0,
			'readfromfile': '',
			'createwavafterfinish': 0,
			'time': 0,
			'data': [],
		
			'': ''
		}

		self.isAlive 	= True
		self.output 	= None
		
	def coreStartRecording(self):
		self.audio = pyaudio.PyAudio()
		 
		self.stream = self.audio.open(format=self.settings['format'], channels=2, rate=self.settings['rate'], input=True, frames_per_buffer=self.settings['chunk'])
		if (self.settings['livefeedback']):
			self.output = self.audio.open(format=self.settings['format'], channels=2, rate=self.settings['rate'], output=True, frames_per_buffer=self.settings['chunk'])
		
		while (self.isAlive):
			data = self.stream.read(self.settings['chunk'])
			if (not self.isAlive): break
			self.settings['data'].append(data)
		
		
		time.sleep(1)
		
		self.stream.stop_stream()
		self.stream.close()
		if (self.settings['livefeedback']):
			self.output.stop_stream()
			self.output.close()
		
		self.audio.terminate()
		
	def clearOldFiles(self):
		temp = open(self.settings['saveto'] + '.raw', 'wb')
		temp.close()
		
	def coreCreateAWavFile(self):
		try:
			waveFile = wave.open(self.settings['saveto'], 'wb')
			waveFile.setnchannels(2)
			waveFile.setsampwidth(self.audio.get_sample_size(self.settings['format']))
			waveFile.setframerate(self.settings['rate'])
			temp = open(self.settings['saveto'] + '.raw', 'rb')
			while (1):
				data = temp.read(1024)
				if (not data): break
				waveFile.writeframes(data)
				
			waveFile.close()
		except:
			print '[-] Failed to save as a wav file.'
		
	def coreWriteToFile(self):
		temp = open(self.settings['saveto'] + '.raw', 'ab')
		temp.write(b''.join(self.settings['data']))
		temp.close()
		self.settings['data'] = []
		
	def coreRecordFor(self):
		Thread(target = self.coreStartRecording).start()
		
		while (self.settings['recordfor'] > 0):
			self.settings['recordfor'] -= self.settings['chunk'] / float(self.settings['rate'])
			
			if (self.settings['livefeedback'] and self.output != None):
				self.output.write(b''.join(self.settings['data']))
			
			if (not self.settings['noautosave']):
				self.coreWriteToFile()
			
			time.sleep(self.settings['chunk'] / float(self.settings['rate']))
		
		
		self.isAlive = 0
		self.coreWriteToFile()
		self.coreCreateAWavFile()

	def coreLoopFile(self, threadStarted = 0):
		while (os.path.isfile(self.settings['readfromfile'])):
			time.sleep( 1 )
			
			try:
				file = open(self.settings['readfromfile'], 'r')
				data = file.read()
				file.close()
				
				for line in data.split('\n'):
					if (len(line) < 4): continue
					key = line.split(':', 1)[0].replace(' ', '')
					value = line.split(':', 1)[1]
					while (value[0] == ' '): value = value[1:1000]
					value = eval(value)
				
					if (self.settings.has_key(key)):
						self.settings[key] = value
				
			except Exception, err:
				print str(err)
				return
			
			if (not threadStarted):
				threadStarted = 1
				self.clearOldFiles()
				Thread(target = self.coreStartRecording).start()
				
				
			try:
				self.coreWriteToFile()
			except:
				break
				
			tm = time.time()
			if (time.time() > self.settings['time']):
				break
		
		self.isAlive = 0
		if (self.settings['createwavafterfinish']):
			self.coreCreateAWavFile()
		
if (__name__ == '__main__'):
	print info, usage

	obj = Main()
	
	if ('--help' in sys.argv):
		sys.exit()
	if ('--rate' in sys.argv):
		obj.settings['rate'] = int( sys.argv[sys.argv.index('--rate') +1 ] )
	if ('--format' in sys.argv):
		obj.settings['format'] = int( sys.argv[sys.argv.index('--format') +1 ] )
	if ('--chunk' in sys.argv):
		obj.settings['chunk'] = int( sys.argv[sys.argv.index('--chunk') +1 ] )
	if ('--recordfor' in sys.argv):
		obj.settings['recordfor'] = int( sys.argv[sys.argv.index('--recordfor') +1 ] )
	if ('--saveto' in sys.argv):
		obj.settings['saveto'] =sys.argv[sys.argv.index('--saveto') +1 ]	
	if ('--noautosave' in sys.argv):
		obj.settings['noautosave'] = 1
	if ('--livefeedback' in sys.argv):
		obj.settings['livefeedback'] = 1
	
	obj.clearOldFiles()
	
	if ('--readfromfile' in sys.argv):
		obj.settings['readfromfile'] =sys.argv[sys.argv.index('--readfromfile') +1 ]	
		obj.coreLoopFile()
	elif (obj.settings['recordfor']):
		obj.coreRecordFor()
		
		
		
		
		
		
		
		
	
