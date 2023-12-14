import urllib.parse as par
import urllib.request as req
import xml.etree.ElementTree
from django.core.management.base import BaseCommand
from reality.models import Reality
import time
import asyncio
import concurrent.futures

class Command(BaseCommand):

    help = "Update building register in danzi (reality model) data"

    def handle(self, *args, **kwargs):

        start = time.time()
        
        print(len(bjdCodeSet))
        loop.run_until_complete(main())
        loop.close()
        print("Working time :", time.time() - start)

loop = asyncio.get_event_loop()
realities = Reality.objects.filter(mgmBldrgstPk__isnull=True)
bjdCodeSet = set(reality.bjdCode for reality in realities)

pool1 = concurrent.futures.ThreadPoolExecutor()
pool2 = concurrent.futures.ThreadPoolExecutor()

async def updateBuildingRegister(bjdCode):
    url = '	http://apis.data.go.kr/1613000/BldRgstService_v2/getBrRecapTitleInfo?'
    serviceKey = 'vDp95sBtTaP3d1x5+mrWmtHmvxzYVS4ni+bIpYXsbnNSpKsUmkUWNPEerkcKYXtVrUwmHTW5Nm0serBgCC1Shg=='
    params ={'serviceKey' : serviceKey, 'sigunguCd' : bjdCode[:5], 'bjdongCd': bjdCode[5:], 'numOfRows': 10000}
    param = par.urlencode(params)

    url = url + param
    response = await loop.run_in_executor(pool1, req.urlopen, url)
    data = await loop.run_in_executor(pool2, response.read)
    await asyncio.sleep(0.25)
    #data = response.read()
    decode = data.decode("utf-8")

    trees = xml.etree.ElementTree.fromstring(decode)
    dataKeys = "mgmBldrgstPk,platArea,archArea,bcRat,totArea,vlRatEstmTotArea,vlRat,hhldCnt,engrGrade".split(",")  

    realityQueryset = Reality.objects.filter(bjdCode = bjdCode)

    for tree in trees[1][0]:
        bun = tree.find('bun').text
        ji = tree.find('ji').text

        dataDict = {}
        for key in dataKeys:
            if tree.find(key) is not None and len(tree.find(key).text.strip()) > 0:
                dataDict[key] = tree.find(key).text

        reality = realityQueryset.filter(bun=int(bun), ji=int(ji)).update(**dataDict)
    
    print(bjdCode)

async def main():
    futures = []
    for bjdCode in bjdCodeSet:
        futures.append(asyncio.ensure_future(updateBuildingRegister(bjdCode)))
        await asyncio.sleep(0.5)

    await asyncio.gather(*futures)