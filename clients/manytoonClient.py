from bs4 import BeautifulSoup
from manhwaDownloader.clients import baseClient


class Client(baseClient.Client):
    """
    subclass of baseClient, specific to manytoons.com
    """

    def __init__(self, siteUrl):
        super().__init__(siteUrl=siteUrl)
        self.site = self.getSite()

    def gatherUrls(self):
        """
        gathers urls from given startUrl and n number of chapter to get
        :param endChapter: int
        :return: list of tupels
        """
        siteUrlList = set()
        if self.site.status_code == 200:
            siteContent = self.site.content
            soup = BeautifulSoup(siteContent, 'html.parser')
            imgTags = soup.find_all('li', {'class': 'wp-manga-chapter'})
            for tag in imgTags:
                rawLink = tag['a']
                cleanLink = rawLink.strip()
                siteUrlList.add(cleanLink)
        return siteUrlList

    def getNextUrl(self):
        """
        get next chapter url
        :return:
        """
        siteUrlList = set()
        if self.site.status_code == 200:
            siteContent = self.site.content
            soup = BeautifulSoup(siteContent, 'html.parser')
            imgTags = soup.find_all('a', {'class': 'btn next_page'})
            for tag in imgTags:
                rawLink = tag['href']
                cleanLink = rawLink.strip()
                siteUrlList.add(cleanLink)
        return siteUrlList

    def run(self):
        siteList = list(self.getNextUrl())
        for site in siteList[:1]:
            print(site)
            siteClient = client.Client(siteUrl=site)
            siteInfoDict = siteClient.gatherSiteInfo()

            ad = asyncioDownloader.AsyncioDownloader(siteInfoDict)
            sites = asyncio.run(ad.createTasks())
            chapterName = [key for key in siteInfoDict.keys()]
            cleanChapterName = re.sub('[^\w\-_\. ]', '', chapterName[0])

            imgNum = 1
            for imgData in sites:
                output.Output(seriesName).toFile(cleanChapterName, imgNum, imgData, saveToProjectFolder=False)
                imgNum += 1
    def gatherSiteInfo(self):
        """
        gather information from given site chapterName, imgNum and imgLink
        :return: dict {chapterName: [(imgNum, imgUrl), ...)]}
        """
        imgInfoDict = dict()
        if self.site.status_code == 200:
            siteContent = self.site.content
            soup = BeautifulSoup(siteContent, 'html.parser')
            chapterTitle = soup.title.string
            imgTags = soup.find_all('img', {'class': 'wp-manga-chapter-img'})
            for tag in imgTags:
                rawLink = tag['src']
                cleanLink = rawLink.strip()

                if not imgInfoDict:
                    imgInfoDict.update({chapterTitle: [cleanLink]})
                else:
                    imgInfoDict[chapterTitle].append(cleanLink)
            return imgInfoDict
