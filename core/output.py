import os
from manhwaDownloader.constants import CONSTANTS as CONST


class Output:
    """
    handels saving images to disk
    """

    def __init__(self, manhwaName):
        self.ouputPath = CONST.OUTPUTPATH
        self.manhwaPath = os.path.join(self.ouputPath, manhwaName)

    def toFile(self, chapterFolderName, imgNum, data, saveToProjectFolder=False):
        """
        method to write to file
        :param chapterFolderName: str
        :param imgNum: int
        :param data: imgData
        :return: None
        """
        chapterFolder = os.path.join(self.manhwaPath, chapterFolderName)
        if saveToProjectFolder:
            chapterFolder = self.manhwaPath

        if imgNum == str:
            imgNum = int(imgNum)

        imageName = f'{imgNum:03d}.jpg'
        if os.path.isdir(chapterFolder):
            with open(os.path.join(chapterFolder, imageName), 'wb') as f:
                f.write(data)
                f.close()
        else:
            os.makedirs(chapterFolder)
            with open(os.path.join(chapterFolder, imageName), 'wb') as f:
                f.write(data)
                f.close()
