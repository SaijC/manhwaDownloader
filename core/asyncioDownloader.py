import aiohttp
import asyncio


class AsyncioDownloader:
    """
    handing image downloads using asyncio package to speed up the process

    ToDo: implement retry when failed
    """

    def __init__(self, siteInfoDict):
        self.siteUrlList = siteInfoDict

    async def readSite(self, session, site):
        """
        Read site content
        :param session: session
        :param site: str
        :return: site content
        """
        async with session.get(site) as response:
            r = await response.read()
            return r

    async def siteLoop(self, session):
        """
        Create asyncio tasks
        :param session: session
        :return: list
        """
        siteContentTask = list()
        for chapterName, siteList in self.siteUrlList.items():
            for link in siteList:
                task = asyncio.create_task(self.readSite(session, link))
                siteContentTask.append(task)
        return await asyncio.gather(*siteContentTask)

    async def createTasks(self):
        """
        Create session
        :return: list
        """
        async with aiohttp.ClientSession() as session:
            sl = await self.siteLoop(session)
            return sl
