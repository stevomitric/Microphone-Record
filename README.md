# Microphone Recorder 
 - A simple Python (2.7.11) implementation of a microphone recorder.
 
	Usage:
  
		sound_record [options]
		
		--rate NUM		- sets recording rate (default: 10000)
		--format NUM		- available: (8 (default), 4, 2)
		--chunk NUM		- Chunk size to read (default: 1024)
		--saveto PATH		- Saves the recording in a file
		--recordfor NUM	- Records for NUM seconds
		--noautosave		- Saves into file after recording is done
		--livefeedback		- Plays audio direcly from microphone
		--readfromfile FILE	- Reads requests from file
		--help			- Displays this info and quits
		
		
		Examples:
			sound_record --rate 40000 --saveto "test.wav" --recordfor 10
			sound_record --saveto "test.wav" --recordfor 20 --livefeedback
			sound_record --readfromfile "C:\programdata\file.txt"
		
		File from "readfromfile" argument, you must define as follows:
		
		time: 2504037551
		rate: 10000
		format: 8
		chunk: 1024
		saveto: "/programdata/sound.wav"
		createwavafterfinish: 0
		
		Time is an argument that defines when the program will stop. You can
		get the value by calling time.time() in python (2.7.11)
		Program will loop as long as you defined all the arguments correcly and
		as long as the file exists in [FILE] path.
		
