from os import *
from shutil import copyfile, move
from time import time

extensions = [".jpg", ".jpeg", ".gif", ".bmp", ".png", ".avi", ".flv", ".wmv", ".mov", ".mp4"]


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

def getFilesOnly(directory, extensions):
	oldDir = getcwd()
	chdir(directory)

	allItems = listdir()
	files = []
	totalSize = 0
	for item in allItems:
		for ext in extensions:
			if(item.endswith(ext)):
				files.append(item)

	chdir(oldDir)
	return files

def totalFileSize(directory, extensions):
	oldDir = getcwd()
	chdir(directory)

	allItems = listdir()
	totalSize = 0
	for item in allItems:
		for ext in extensions:
			if(item.endswith(ext)):
				totalSize += stat(getcwd()+"/"+item).st_size

	chdir(oldDir)
	return totalSize

def organize(destDirectory, extensions):
	subDirSize = int(input("Maximum size(in bytes) of each folder: "))

	chdir(destDirectory)
	files = getFilesOnly(getcwd(), extensions)
	totalSize = totalFileSize(getcwd(), extensions)
	subDirCount = 1
	makedirs(destDirectory+"/"+str(subDirCount))
	while(totalSize>0):
		if(totalFileSize(destDirectory+"/"+str(subDirCount), extensions) + stat(destDirectory+"/"+files[0]).st_size < subDirSize):
			totalSize -= stat(destDirectory+"/"+files[0]).st_size
			move(getcwd()+"/"+files[0], getcwd()+"/"+str(subDirCount)+"/"+files[0])
			files.remove(files[0])

		else:
			subDirCount += 1
			makedirs(destDirectory+"/"+str(subDirCount))



mode = input("Default or manual mode?").lower()
if(mode=="test"):
	rootDir = "C:/Users/Jackson/Documents/hackathonTest"
	destDirectory = "C:/Users/Jackson/Desktop/Photos-Found"
elif(mode=="manual"):
	rootDir = input("Enter path to root folder\n")
	destDirectory = input("Enter path to destination folder:\n")		
else:
	lastDir = getcwd()
	while(not getcwd().endswith("Users")):
		lastDir = getcwd()
		chdir("..")
	rootDir = getcwd()
	destDirectory = lastDir + "/Desktop/Photos-Found"

if(not path.isdir(destDirectory)):
	makedirs(destDirectory)

for ext in extensions:
	FindType(ext, rootDir, destDirectory)


print("Process complete: ", filesFound, "files were found.")

organize(destDirectory, extensions)