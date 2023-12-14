import urllib.parse as par
import urllib.request as req
import xml.etree.ElementTree
from django.core.management.base import BaseCommand
from reality.models import Reality
import time
import asyncio
import concurrent.futures

class Command(BaseCommand):

    help = "Add address in danzi (reality model) data"

    def handle(self, *args, **kwargs):

        start = time.time()
        
        loop.run_until_complete(main())
        loop.close()
        print("Working time :", time.time() - start)

loop = asyncio.get_event_loop()
realities = Reality.objects.filter(kaptAddr__isnull=True)

pool1 = concurrent.futures.ThreadPoolExecutor()
pool2 = concurrent.futures.ThreadPoolExecutor()
pool3 = concurrent.futures.ThreadPoolExecutor()
pool4 = concurrent.futures.ThreadPoolExecutor()

async def updateDanziData(kaptCode):
    url = 'http://apis.data.go.kr/1613000/AptBasisInfoService1/getAphusBassInfo?'
    serviceKey = 'vDp95sBtTaP3d1x5+mrWmtHmvxzYVS4ni+bIpYXsbnNSpKsUmkUWNPEerkcKYXtVrUwmHTW5Nm0serBgCC1Shg=='
    params ={'serviceKey' : serviceKey, 'kaptCode' : kaptCode}
    param = par.urlencode(params)

    url = url + param
    response = await loop.run_in_executor(pool1, req.urlopen, url)
    data = await loop.run_in_executor(pool2, response.read)
    #data = response.read()
    decode = data.decode("utf-8")

    trees = xml.etree.ElementTree.fromstring(decode)

    dataDict = {}
    dataKeys = "bjdCode,codeAptNm,codeGarbage,codeHallNm,codeHeatNm,codeMgrNm,codeNet,codeSaleNm,codeStr,convenientFacility,doroJuso,educationFacility,hoCnt,kaptAcompany,kaptAddr,kaptBcompany,kaptdaCnt,kaptdCccnt,kaptdEcnt,kaptDongCnt,kaptdPcnt,kaptdPcntu,kaptdWtimebus,kaptdWtimesub,kaptFax,kaptMarea,kaptMparea_135,kaptMparea_136,kaptMparea_60,kaptMparea_85,kaptName,kaptTarea,kaptTel,kaptUrl,kaptUsedate,privArea,subwayLine,subwayStation,welfareFacility".split(",")
    for key in dataKeys:
        if trees[1][0].find(key) is not None and len(trees[1][0].find(key).text.strip()) > 0:
            if key == 'kaptdCccnt':
                dataDict[key] = round(float(trees[1][0].find(key).text))
            else:
                dataDict[key] = trees[1][0].find(key).text
    

    url = 'http://apis.data.go.kr/1613000/AptBasisInfoService1/getAphusDtlInfo?'
    
    url = url + param
    response = await loop.run_in_executor(pool3, req.urlopen, url)
    #response = req.urlopen(url)
    data = await loop.run_in_executor(pool4, response.read)
    decode = data.decode("utf-8")
    trees = xml.etree.ElementTree.fromstring(decode)

    for key in dataKeys:
        if key not in dataDict and trees[1][0].find(key) is not None and len(trees[1][0].find(key).text.strip()) > 0:
            if key == 'kaptdCccnt':
                dataDict[key] = round(float(trees[1][0].find(key).text))
            else:
                dataDict[key] = trees[1][0].find(key).text
    
    reality = Reality.objects.filter(kaptCode=kaptCode)
    print(reality.first().id,":", kaptCode)
    if reality.exists():
        reality.update(**dataDict)
        print("성공")
    else:
        print("실패")

async def main():
    futures = []
    for reality in realities:
        futures.append(asyncio.ensure_future(updateDanziData(reality.kaptCode)))
        await asyncio.sleep(0.5)
    await asyncio.gather(*futures)