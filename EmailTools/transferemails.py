import os
import multiprocessing
import shutil

def flatreturn(directory):
	'''moves files from the given directory, calls itself on lower directories.
	
	:param directory: A directory path
	
	:returns: None
	
	>>> flatreturn(/usr/):
	
	'''
	filelst = os.listdir(directory)
	
	for file in filelst:
		if os.path.isdir(directory + "/" + file):
			flatreturn(directory + "/" + file)
		else:
			shutil.copy(directory + "/" + file,"../Emails/%s-%s" % (directory[-3:],file))
	
flatreturn("../TRANSFER")
