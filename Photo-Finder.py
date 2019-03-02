from os import *
from shutil import copyfile
from time import time

lastUpdated = time()

filesFound = 0

def updateCount():
	global lastUpdated
	global filesFound

	if (time()-lastUpdated>10):
		print(filesFound, "files found so far...")
		lastUpdated = time()

def FindType(FileExtension, root, destination):
	global filesFound
	chdir(root)
	dirs = []

	try:
		all = listdir()
		for name in all:
			if(name.endswith(FileExtension)):
				copyfile(getcwd()+"/"+name, destination+"/"+name)
				filesFound += 1
			if(path.isdir(getcwd()+"/"+name) and (getcwd()+"/"+name != destination)):
				dirs.append(name)

		for subdir in dirs:
			FindType(FileExtension, subdir, destination)
	except:
		filesFound+=0
	updateCount()
	chdir("..")
	# end of FindType()



mode = input("Default or manual mode?")
if(mode.lower()=="manual"):
	rootDir = input("Enter path to root folder\n")
	destDirectory = input("Enter path to destination folder:\n")
	if(rootDir.lower()=="test"):
		rootDir = "C:/Users/Jackson/Documents/hackathonTest"
	if(destDirectory.lower()=="test"):
		destDirectory = "C:/Users/Jackson/Desktop/Photos-Found"
else:
	lastDir = getcwd()
	while(not getcwd().endswith("Users")):
		lastDir = getcwd()
		chdir("..")
	rootDir = getcwd()
	destDirectory = lastDir + "/Desktop/Photos-Found"


if(not path.isdir(destDirectory)):
	makedirs(destDirectory)

extensions = [".jpg", ".jpeg", ".gif", ".bmp", ".png", ".avi", ".flv", ".wmv", ".mov", ".mp4"]

for ext in extensions:
	FindType(ext, rootDir, destDirectory)


print("Process complete: ", filesFound, "files were found.")