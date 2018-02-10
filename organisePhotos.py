import os
import shutil
from PIL import Image, ExifTags
from datetime import datetime

# issues to deal with:
# different file types: videos - currently just coping them all to one folder 
# currently only dealing with jpg and mp4 - might have to allow for other file types
# duplicates: currently duplicates are not dealt with - build in a reporting tool for this
# does not deal with subfolders within initial directories
# develop a final check to make sure all items within a folder have been dealt with
# report back on number of copied file after copying each folder, rather than at the end

years = ['2012','2013','2014','2015','2016','2017','2018']                           # is there a datetime function for this?
months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']   # is there a datetime function for this?

##################################

def createFolder(newDirName):
    """ create a folder with the folder name of the passed in parameter """
    """ expand this function to include a check to see if the path exists already - if so, then do not create """
    print "creating folder for %s" %(newDirName)
    try:
        os.makedirs(newDirName)
    except OSError:
        if not os.path.isdir(newDirName):
            raise   

##################################

def makeYearMonthFolders(rootPictureDirectory):
# call the function to create folders based on the parameters of year and months
     videoDir = os.path.join(rootPictureDirectory,"Videos")
     createFinalFolder(videoDir)
     for year in years:
         dirName = os.path.join(rootPictureDirectory,year)
         createFolder(dirName)
         for month in months:
             createFolder(os.path.join(dirName +"\\" + str(month)))   # can I change this to dirName,month ???? 
         print 

#################################

def copyFilesToOrderedDirs(pictureDirectories):
# function that takes input directories with pictures, runs through each picture image,
# isolates the image's capture month and year, and then copies the image to the 
# appropriate folder to store it based on the capture date

     count = 0
     notCopiedCount = 0
     try: 
          for picDir in pictureDirectories:
               print "Processing files from %s" %(picDir)
               for root, dirs, files in os.walk(picDir):
                    for filename in files:
                         idFilename = filename.split(os.extsep)[1]
                         if idFilename == 'jpg':
                             fullPictureLocation = os.path.join(root,filename)
                             img = Image.open(fullPictureLocation)
                             exif = { ExifTags.TAGS[k]: v for k,
                             v in img._getexif().items() if k in ExifTags.TAGS }
                             for k,v in exif.items():#
                                  # isolate the DateTime key in the dict
                                  if k == "DateTime":
                                       captureDate = datetime.strptime(str(v), '%Y:%m:%d %H:%M:%S')
                                       captureMonth = captureDate.strftime("%b")
                                       captureYear = captureDate.strftime("%Y")
                                       # create dir path where to copy the image into
                                       copyToPath = os.path.join(rootPictureDirectory,captureYear,captureMonth)
                                       shutil.copy2(os.path.join(root, filename), os.path.join(copyToPath, filename))
                                       count = count+1
                         elif idFilename == 'mp4':
                            copyToPath = os.path.join(rootPictureDirectory,'Videos')
                            shutil.copy2(os.path.join(root, filename), os.path.join(copyToPath, filename))
                            count = count+1
          print "Number of files copied: %s" % count 
          print "Number of files not copied: %s" % notCopiedCount 
     except Exception, e:
          print "Number of files copied before exception raised: %s" % count
          raise e

############################################

rootPictureDirectory = "E:\Pictures_Organised10022018" # root folder where images will be copied to
listPictureDirectories = ["E:\JordanCameraPhotos"] # list of directories to read images from

#createFinalFolders = makeYearMonthFolders(rootPictureDirectory)

runOrderingOfPics = copyFilesToOrderedDirs(listPictureDirectories)

#processedFolders = "E:\picturesFromPhone09102017", "E:\picturesFromPhone211015", "E:\picturesFromPhone16052016","E:\picturesFromPhone26012017","E:\picturesFromPhone30012016"