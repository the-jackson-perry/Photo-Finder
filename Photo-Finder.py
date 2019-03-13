from os import *
from shutil import copyfile, move
from tkinter import *


def FindType(FileExtension, rootDir, destination):
	global filesFound
	global root
	chdir(rootDir)
	dirs = []

	try:
		all = listdir()
		for name in all:
			if(name.endswith(FileExtension)):
				copyfile(getcwd()+"/"+name, destination+"/"+name)
				filesFound.set(filesFound.get()+1)
				root.update()
			if(path.isdir(getcwd()+"/"+name) and (getcwd()+"/"+name != destination)):
				dirs.append(name)

		for subdir in dirs:
			FindType(FileExtension, subdir, destination)
	except:
		filesFound.get()
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
	# end of getFilesOnly()

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
	# end of totalFileSize()

def makeSubDirs(destDirectory, extensions, subDirSize):
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
		elif(stat(destDirectory+"/"+files[0]).st_size>subDirSize):
			files.remove(files[0])
		else:
			subDirCount += 1
			makedirs(destDirectory+"/"+str(subDirCount))
	# end of organize()

def getDefaultRoot():
	originalDir = getcwd()

	lastDir = getcwd()
	while(not getcwd().endswith("Users")):
		lastDir = getcwd()
		chdir("..")
	rootDir = lastDir

	chdir(originalDir)
	return rootDir
	# end of getDefaultRoot()

def getDefaultDestination():
	originalDir = getcwd()

	lastDir = getcwd()
	while(not getcwd().endswith("Users")):
		lastDir = getcwd()
		chdir("..")
	destDirectory = lastDir + "\\Desktop\\Photos-Found"
	
	chdir(originalDir)
	return destDirectory
	# end of getDefaultDestination()

def start(root,setupFrame,rootDirEntry,destDirEntry,extensions,putInSubDirs,mbChecked,subDirSizeEntry):
	global filesFound

	rootDir = rootDirEntry.get()
	destDirectory = destDirEntry.get()
	subDirSize = float(subDirSizeEntry.get())

	setupFrame.pack_forget()
	setupFrame.destroy()

	searchFrame = Frame(root)
	Label(searchFrame, text="Searching...Files found: ").pack(side=LEFT)
	Label(searchFrame, textvariable=filesFound).pack(side=LEFT)
	searchFrame.pack()
	root.update()

	if(not path.isdir(destDirectory)):
		makedirs(destDirectory)

	for ext in extensions:
		FindType(ext, rootDir, destDirectory)

	print("Process complete: ", filesFound.get(), "files were found.")
	#closeSearchingWindow()

	
	if(putInSubDirs):
		if(mbChecked):
			subDirSize = int(subDirSize * 1000000)
		else:
			subDirSize = int(subDirSize * 1000000000)

		makeSubDirs(destDirectory, extensions, subDirSize)
		print("Process complete: files were put in sub-directories.")
	exit(0)
	# end of start()

###############################################################################################

extensions = [".jpg", ".jpeg", ".gif", ".bmp", ".png", ".avi", ".flv", ".wmv", ".mov", ".mp4"]

root = Tk()
root.title("Photo-Finder")

filesFound = IntVar()
filesFound.set(0)

setupFrame = Frame(root)

pathInputFrame = Frame(setupFrame)

Label(pathInputFrame, text="Path to directory that will be searched (default is to search everything for the current user):").grid(row=0, sticky=W)
rootDirEntry = Entry(pathInputFrame, width=100)
rootDirEntry.insert(0, getDefaultRoot())
rootDirEntry.grid(row=1, sticky=W)

Label(pathInputFrame, text="Path to destination directory (default is a folder created on your Desktop):").grid(row=4, sticky=W)
destDirEntry = Entry(pathInputFrame, width=100)
destDirEntry.insert(0, getDefaultDestination())
destDirEntry.grid(row=5, sticky=W)

optionsFrame = Frame(setupFrame)
Label(optionsFrame, text="Additional options:").grid(row=0, sticky=W)
showPreviews = BooleanVar()
showPreviews.set(False)
putInSubDirs = BooleanVar()
putInSubDirs.set(False)
Checkbutton(optionsFrame, variable=showPreviews, text="Show preview of picture before adding to destination folder?").grid(row=1, sticky=W)
Checkbutton(optionsFrame, variable=putInSubDirs, text="Divide files into sub-folders").grid(row=2, sticky=W)
Label(optionsFrame, text="Maximum size of each sub-folder:").grid(row=3, sticky=W)

maxFolderFrame = Frame(optionsFrame)
subDirSizeEntry = Entry(maxFolderFrame, width = 10)
subDirSizeEntry.insert(0, "0")
subDirSizeEntry.grid(row=0, column=0)
mbChecked = BooleanVar()
mbChecked.set(True)
mb = Radiobutton(maxFolderFrame, variable=mbChecked, value=1, text="MegaBytes").grid(row=0, column=1, sticky=W)
gb = Radiobutton(maxFolderFrame, variable=mbChecked, value=0, text="GigaBytes").grid(row=0, column=2, sticky=W)
maxFolderFrame.grid(row=4, sticky=W)

pathInputFrame.grid(row=0)
optionsFrame.grid(row=1)
startButton = Button(setupFrame, text="Find Files", command= lambda: start(root,setupFrame,rootDirEntry,destDirEntry,extensions,putInSubDirs.get(),mbChecked.get(),subDirSizeEntry))
startButton.grid(row=2)


setupFrame.pack()

root.mainloop()
###########################################################################