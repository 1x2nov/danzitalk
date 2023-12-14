import urllib.parse as par
import urllib.request as req
import xml.etree.ElementTree
from django.core.management.base import BaseCommand
from reality.models import Reality
import time
import requests
import asyncio
import concurrent.futures

class Command(BaseCommand):

    help = "Add Coordinate (x,y) in danzi (reality model) data"

    def handle(self, *args, **kwargs):

        start = time.time()

        loop.run_until_complete(main())
        loop.close()

        print("Working time :", time.time() - start)

loop = asyncio.get_event_loop()
realities = Reality.objects.filter(x=0.0,y=0.0).exclude(kaptAddr__isnull=True)

async def addCoor(id, kaptAddr, kaptName, doroJuso):

    url = 'https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode?'
    apikeyid = 'uchpw1zwm9'
    apikey = 'CoTg0RsZ0iHA1QLW9HlZZnBLporfEUQhF7S8YBN1'
    headers ={
        'X-NCP-APIGW-API-KEY-ID' : apikeyid,
        'X-NCP-APIGW-API-KEY' : apikey,
        'Accept' : 'application/xml'
    }

    f = lambda params : requests.get(url, headers=headers, params=params)

    try:
        response = await loop.run_in_executor(None, f, {'query' : kaptAddr})
        trees = xml.etree.ElementTree.fromstring(response.text)

        x = trees[2].find('x').text
        y = trees[2].find('y').text

    except:
        try:
            response = await loop.run_in_executor(None, f, {'query' : kaptAddr.replace(kaptName, "").strip()})
            trees = xml.etree.ElementTree.fromstring(response.text)

            x = trees[2].find('x').text
            y = trees[2].find('y').text
        
        except:
            try:
                response = await loop.run_in_executor(None, f, {'query' : doroJuso})
                trees = xml.etree.ElementTree.fromstring(response.text)

                x = trees[2].find('x').text
                y = trees[2].find('y').text
            
            except:
                print("실패:", id, kaptAddr)
                return False

    Reality.objects.filter(id=id).update(x=x,y=y)

    print("완료:", id, kaptAddr)
    return True

async def main():

    futures = [asyncio.ensure_future(addCoor(reality.id, reality.kaptAddr, reality.kaptName, reality.doroJuso)) for reality in realities]

    await asyncio.gather(*futures)