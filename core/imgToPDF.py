import os
import shutil

from PIL import Image
from manhwaDownloader.constants import CONSTANTS as CONST


class ImgToPDF:
    """
    class to handel pdf conversion
    """

    def __init__(self, manhwaName):
        self.ouputPath = CONST.OUTPUTPATH
        self.manhwaPath = os.path.join(self.ouputPath, manhwaName)

    def _iterateFoldersForFiles(self, inProjectFolder=False):
        """
        walk through the folder tree and construc a dictionary representation of the folder structure
        :param inProjectFolder: bool
        :return: dict {folderPath: [list of files]}
        """
        chapterDicts = dict()

        if inProjectFolder:
            for file in os.listdir(self.manhwaPath):
                truncatedPath = os.path.join(self.manhwaPath, file)
                fullPath = os.path.abspath(truncatedPath)
                if os.path.isfile(fullPath):
                    if not chapterDicts:
                        chapterDicts.update({self.manhwaPath: [file]})
                    else:
                        chapterDicts[self.manhwaPath].append(file)
        else:
            walkList = [file for file in os.walk(self.manhwaPath)]
            for folder, _, files in walkList[1:]:
                chapterDicts.update({folder: files})
        return chapterDicts

    def _imgCrop(self, im, top, bottom, cropedImgList):
        """
        cropping an image
        :param im: PIL object
        :param top: int
        :param bottom: int
        :param cropedImgList: list 
        :return: None
        """
        width, height = im.size
        imgHeight = 2500

        if height - bottom <= 0:
            top = top + 1
            im1 = im.crop((0, top, width, bottom))

            cropedImgList.append(im1)
        elif top == 0:
            im1 = im.crop((0, 0, width, imgHeight))
            cropedImgList.append(im1)
            self._imgCrop(im, imgHeight, imgHeight * 2, cropedImgList)
        else:
            top = top + 1
            im1 = im.crop((0, top, width, bottom))
            cropedImgList.append(im1)
            self._imgCrop(im, top + imgHeight, bottom + imgHeight, cropedImgList)

    def deleteAllPDF(self, inProjectFolder=False):
        """
        Delete all PDFs
        :param inProjectFolder: bool search all project folder
        :return: None
        """
        folderDict = self._iterateFoldersForFiles(inProjectFolder)
        for folderPath, filesList in folderDict.items():
            if os.path.isdir(folderPath):
                for file in filesList:
                    logging.info(folderPath)
                    fullPath = os.path.join(folderPath, file)
                    extension = fullPath.split('.')[-1]
                    if extension in CONST.GREENLIST:
                        os.remove(fullPath)
        logging.info('All PDFs removed!')

    def deleteAllImg(self, inProjectFolder=False):
        """
        Delete all image files
        :param inProjectFolder: bool search all project folder
        :return: None
        """
        folderDict = self._iterateFoldersForFiles(inProjectFolder)
        for folderPath, filesList in folderDict.items():
            if os.path.isdir(folderPath):
                for file in filesList:
                    logging.info(folderPath)
                    fullPath = os.path.join(folderPath, file)
                    extension = fullPath.split('.')[-1]
                    if extension in CONST.GREENLIST:
                        os.remove(fullPath)
        logging.info('All images removed!')

    def deleteAllFolders(self, inProjectFolder=False):
        """
        delete all folders in the project
        :param inProjectFolder: bool search all project folder
        :return:
        """
        folderDict = self._iterateFoldersForFiles(inProjectFolder)
        for folderPath, filesList in folderDict.items():
            shutil.rmtree(folderPath, ignore_errors=True)
            logging.info('All project removed!')

    def cropLargeImges(self, inProjectFolder=False):
        """
        crop images that are too big < 14000px
        :param inProjectFolder: bool search all project folder
        :return:
        """
        folderDict = self._iterateFoldersForFiles(inProjectFolder)
        for folderPath, filesList in folderDict.items():
            if os.path.isdir(folderPath):
                imgNum = 1
                originalImg = list()
                for file in filesList:
                    cropedImgList = list()
                    fullPath = os.path.join(folderPath, file)
                    extension = fullPath.split('.')[-1]

                    if extension in CONST.GREENLIST:
                        image1 = Image.open(fullPath)
                        width, height = image1.size
                        if height > 14000:
                            originalImg.append(fullPath)
                            self._imgCrop(image1, 0, 2500, cropedImgList)

                        for img in cropedImgList:
                            img.save(f'{folderPath}\\{imgNum:03d}_CROPPED.jpg')
                            imgNum += 1

                for img in originalImg:
                    os.remove(os.path.join(folderPath, img))

    def convertToPDF(self, inProjectFolder=False):
        """
        Convert images to pdf
        :return: None
        """
        folderDict = self._iterateFoldersForFiles(inProjectFolder)
        for folderPath, filesList in folderDict.items():
            if os.path.isdir(folderPath):
                convertedImgList = list()
                for file in filesList:
                    fullPath = os.path.join(folderPath, file)
                    extension = fullPath.split('.')[-1]
                    if extension in CONST.GREENLIST:
                        image1 = Image.open(fullPath)
                        im1 = image1.convert('RGB')
                        convertedImgList.append(im1)
                chapterName = folderPath.split('\\')[-1]
                pdfName = f'{chapterName}.pdf'
                pdfPath = os.path.join(folderPath, pdfName)

                if not os.path.exists(pdfPath):
                    logging.info(f'converting: {pdfName}')
                    convertedImgList[0].save(pdfPath,
                                             save_all=True,
                                             append_images=convertedImgList[1:])
                else:
                    logging.info(f'file exists SKIPPING: {pdfName}')

    def checkImgFiles(self, inProjectFolder=False):
        """
        Check all images to ensure they downloaded properly
        :param inProjectFolder: bool search all project folder
        :return: list/None
        """
        issueImgs = list()
        folderDict = self._iterateFoldersForFiles(inProjectFolder)
        for folderPath, filesList in folderDict.items():
            if os.path.isdir(folderPath):
                for file in filesList:
                    fullPath = os.path.join(folderPath, file)
                    extension = fullPath.split('.')[-1]
                    if not extension == 'pdf':
                        try:
                            Image.open(fullPath)
                        except:
                            issueImgs.append(fullPath)
        return issueImgs

    def removeStrFromName(self, subString=None):
        """
        removes string from folder
        :param subString: str
        :return: None
        """
        for dir in os.listdir(self.manhwaPath):
            path = os.path.join(self.manhwaPath, dir)
            if os.path.isdir(path):
                newPathName = path.replace(subString, '').strip()
                os.rename(path, newPathName)

    def movePDFtoParentFolder(self, inProjectFolder=False):
        """
        Move all PDFs to parent folder
        :param inProjectFolder: bool search all project folder
        :return: None
        """
        folderDict = self._iterateFoldersForFiles(inProjectFolder)
        for folderPath, filesList in folderDict.items():
            if os.path.isdir(folderPath):
                for file in filesList:
                    fullPath = os.path.join(folderPath, file)
                    extension = fullPath.split('.')[-1]
                    if extension == 'pdf':
                        shutil.move(fullPath, self.manhwaPath)

    def run(self, removeStrFromName='', inProjectFolder=False, deleteFolders=False):
        """
        utility method, run a series of class methods
        :param inProjectFolder: bool search all project folder
        :return: None
        """
        check = self.checkImgFiles(inProjectFolder)
        if check:
            return check
        else:
            self.cropLargeImges()
            if removeStrFromName:
                self.removeStrFromName(removeStrFromName)
            self.convertToPDF(inProjectFolder)
            self.movePDFtoParentFolder(inProjectFolder)
            if deleteFolders:
                self.deleteAllFolders()


converter = ImgToPDF('a-wonderful-new-world')
print(converter.run())
