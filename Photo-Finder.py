from os import *
from shutil import copyfile
from time import time

lastUpdated = time()

filesFound = 0

def updateCount():
	global lastUpdated
	global filesFound

	if (time()-lastUpdated>10):
		print(filesFound, "files found...")
		lastUpdated = time()

def FindType(FileExtension, root, destination):
	global filesFound
	updateCount()
	chdir(root)
	dirs = []

	try:
		all = listdir()
		for name in all:
			if(name.endswith(FileExtension)):
				copyfile(getcwd()+"/"+name, destDirectory+"/"+name)
				filesFound += 1
			if(path.isdir(getcwd()+"/"+name)):
				dirs.append(name)

		for subdir in dirs:
			FindType(FileExtension, subdir, destination)
	except:
		updateCount()

	chdir("..")
	# end of FindType()



mode = input("Default or manual mode?")
if(mode.lower()=="default"):
	destDirectory = "C:/Users/Jackson/Desktop/Photos_Found"
	rootDir = "C:/Users"
else:
	rootDir = input("Enter path to root folder\n")
	destDirectory = input("Enter path to destination folder:\n")


if(not path.isdir(destDirectory)):
	makedirs(destDirectory)

extensions = [".jpg", ".jpeg", ".gif", ".bmp", ".png"]

for ext in extensions:
	FindType(ext, rootDir, destDirectory)