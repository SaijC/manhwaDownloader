import requests
import logging
import cfscrape
import os
from manhwaDownloader.constants import CONSTANTS as CONST

logging.basicConfig(level=logging.DEBUG)

folderPath = os.path.join(CONST.OUTPUTPATH, 'serious-taste-of-forbbiden-fruit')

logging.info(len([file for file in os.walk(folderPath)]))
walkList = [file for file in os.walk(folderPath)]

chapterDicts = dict()

for folder, _, files in walkList[1:]:
    chapterDicts.update({folder: files})

print(chapterDicts)