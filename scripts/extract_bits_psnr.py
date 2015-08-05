import subprocess
import time
import re
import sys

#enviroment HM and where sequences are stored
main_path = '/home/daniel/HM-16.0/'
sequences_path = '/home/daniel/origCfP/'

#attributes to change between different simulations scenarios
nFrames = 10
AC_Algorithm = 0
AC_Data = 0

#regular expressions to extract results from encoding
re_bits = re.compile('\d+\s*a\s*([0-9.]*)\s*')
re_psnr = re.compile('\d+\s*a\s*[0-9.]*\s*([0-9.]*)')

#paths in the HM folder tree
encoder_path = main_path + 'bin/TAppEncoderStatic'
cfg_structure_path = main_path + 'cfg/encoder_lowdelay_P_main_2Ref.cfg'
cfg_sequences_path = main_path+'cfg/per-sequence/'

#some arguments that are fixed for all simulations
list_of_fixed_arguments = ['--FramesToBeEncoded='+str(nFrames),'--HadamardME=0','--FEN=0', '--FDM=0']

list_of_QPs = [
				22
				,27
				,32
				,37
				]

list_of_sequences = [	
					'BQMall_832x480_60.yuv'
					,'BQTerrace_1920x1080_60.yuv'
					,'BasketballDrive_1920x1080_50.yuv'
					,'BasketballDrill_832x480_50.yuv'
					,'RaceHorses_832x480_30.yuv'
					,'Cactus_1920x1080_50.yuv'
					]

list_of_cfg_sequences = [
						'BQMall.cfg'
						,'BQTerrace.cfg'
						,'BasketballDrive.cfg'
						,'BasketballDrill.cfg'
						,'RaceHorsesC.cfg'
						,'Cactus.cfg'
						]


#call encoder as a subprocess
for (sequence, cfg_sequence) in zip(list_of_sequences, list_of_cfg_sequences):
	all_bits = []
	all_psnr = []
	for qp in list_of_QPs:

		arguments = [encoder_path,'-c',cfg_structure_path,'-c',cfg_sequences_path+cfg_sequence,'--InputFile='+sequences_path+sequence, '--QP='+str(qp), '--AC_DataLevel=0', '--AC_AlgorithmLevel=0']+list_of_fixed_arguments
		
		# print command line
		# sys.stdout.write('#')
		# for token in arguments:
		# 	sys.stdout.write(token+' ')
		# print 

		#call encoder as subprocess and save output to proc_encoder.stdout to parse and get information
		proc_encoder = subprocess.Popen(arguments,stdout=subprocess.PIPE)
		proc_encoder.wait()

		#parse output to get bits and psnr from proc_encoder.stdout file
		encoder_output = proc_encoder.stdout.read()
		m = re_bits.search(encoder_output)
		if m:
			all_bits.append(m.group(1))
		else:
			print "ERROR on parsing bits"
		m = re_psnr.search(encoder_output)
		if m:
			all_psnr.append(m.group(1))
		else:
			print "ERROR on parsing psnr"
		
	print sequence
	print 'qp', 'bits_ref', 'psnr_ref', 'bits_AC', 'psnr_AC'
	for bits, psnr, qp in zip(all_bits,all_psnr,list_of_QPs):		
		print qp, bits, psnr

# #read temperature while encoder subprocess is not finished
# core0 = []
# core1 = []
# core2 = []
# core3 = []
# while proc_encoder.poll() != 0:
# 	proc_sensors = subprocess.Popen(['sensors'],stdout=subprocess.PIPE)

# 	lines = proc_sensors.stdout.readlines()
# 	#print lines[8].split()[0]+lines[8].split()[1][:-1] + ' ' + lines[8].split()[2][1:-2]
# 	core0.append(lines[8].split()[2][1:-3])
# 	#print lines[9].split()[0]+lines[9].split()[1][:-1] + ' ' + lines[9].split()[2][1:-2]
# 	core1.append(lines[9].split()[2][1:-2])
# 	#print lines[10].split()[0]+lines[10].split()[1][:-1] + ' ' + lines[10].split()[2][1:-2]
# 	core2.append(lines[10].split()[2][1:-2])
# 	#print lines[11].split()[0]+lines[11].split()[1][:-1] + ' ' + lines[11].split()[2][1:-2]
# 	core3.append(lines[11].split()[2][1:-2])

# 	time.sleep(1)

# for temp in core0:
# 	print temp