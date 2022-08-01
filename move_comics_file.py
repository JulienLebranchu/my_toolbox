from __future__ import print_function
import os, re, shutil

PATTERN = "[0-9]*-(.*)#"
PATTERN = "[0-9]*-([^#0-9]*).*$"

class MoveFile(object):
    def __init__(self, srcDir, dstDir, recursive=False, flag='.CBZ'):
        self.srcDir = srcDir
        self.dstDir = dstDir
        self.recursive = recursive
        self.flag = flag
        self.duplicateFileName = []
        self.badFileName = []
        self.flagFile = []
        self.srcDirDict = {}

    def findAllFile(self):
        # recursively find file 
        if self.recursive == False:        
            for item in os.listdir(self.srcDir):
                if os.path.isfile(os.path.join(self.srcDir,item)) and \
                                os.path.splitext(item)[-1] == self.flag.lower():
                    self.flagFile.append(item)
                    self.srcDirDict[item] = self.srcDir
        else:
            for root, dirs, files in os.walk(self.srcDir):
                for item in files:
                    if os.path.splitext(item)[-1] == self.flag.lower():
                        self.flagFile.append(item)
                        self.srcDirDict[item] = root

        if not self.flagFile: 
            print('NOT FIND ANY %s FILE!', self.flag)
        return self.flagFile

    def parse(self, text):
        print(text)
        try:
            pat =re.compile(PATTERN)
            match = pat.match(text)
            data = None
            fileName=None
            if match != None:
                data = match.group(1)
                fileName = data
            
            
        except TypeError:
            self.badFileName.append(text)
            fileName = None
        return fileName  

    def move(self, text):
        
        try:
            fileName = self.parse(text)
            if fileName == None: return
            
            print()
            if not os.path.isdir(os.path.join(self.dstDir, fileName)):
                os.mkdir(os.path.join(self.dstDir,fileName))
                
            srcPath= os.path.join(self.srcDirDict[text], text)
            dstDir = os.path.join(self.dstDir, fileName)
            shutil.move(srcPath, dstDir)
        except:
            self.duplicateFileName.append(text)
            raise

    @staticmethod
    def decC(dir):
        return os.path.join(self.srcDir,dir)

    def run(self):
        try:
            if not os.path.isdir(self.dstDir):
                os.mkdir(self.dstDir)
            for text in self.findAllFile():
                self.move(text)
            print('MOVE SUCCESSFUL!') 
        except:
            raise

srcDir = r'/Users/jlebranc/Documents/Perso/Comics/DC Comics Intégrale Rebirth - 2723 tomes'
srcDir = r'/Users/jlebranc/Documents/Perso/Comics/DC Comics Intégrale New 52 - 3131 tomes'
dstDir = srcDir
fmv = MoveFile(srcDir, dstDir, recursive = False)

fmv.run()