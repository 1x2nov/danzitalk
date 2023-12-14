import urllib.parse as par
import urllib.request as req
import xml.etree.ElementTree
from django.core.management.base import BaseCommand
from reality.models import Reality, LinkerRTMS, RTMSRent
import time
import itertools

sggCodeSet = set(reality.bjdCode[:5] for reality in Reality.objects.all())

class Command(BaseCommand):

    help = "Add RTMS Rent data"

    def handle(self, *args, **kwargs):

        start = time.time()

        productSet = set(itertools.product(range(2018, 2022+1), range(1, 12+1), sggCodeSet))

        try:
            f = open('complete_rtmsrent.info', 'r')
            lines = f.readlines()
            f.close()
        except:
            lines = []

        for line in lines:
            y, m, sggCode = line.split()
            productSet.remove((int(y),int(m),sggCode))
        
        for y, m, sggCode in sorted(list(productSet), reverse=True)[:50]:
            dealYMD = "{0}{1:02d}".format(y,m)
            addrtms(sggCode, dealYMD)

        print("Working time :", time.time() - start)

def addrtms(sggCode, dealYMD):
    url = 'http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptRent?'
    serviceKey = 'vDp95sBtTaP3d1x5+mrWmtHmvxzYVS4ni+bIpYXsbnNSpKsUmkUWNPEerkcKYXtVrUwmHTW5Nm0serBgCC1Shg=='
    params ={'serviceKey' : serviceKey, 'DEAL_YMD' : dealYMD, 'LAWD_CD': sggCode}
    param = par.urlencode(params)

    url = url + param
    response = req.urlopen(url)
    data = response.read()
    decode = data.decode("utf-8")

    trees = xml.etree.ElementTree.fromstring(decode)

    for tree in trees[1][0]:
        if tree.find('지번') is None:
            continue
        bjd = tree.find('법정동').text.strip()
        jibun = tree.find('지번').text.strip().replace('산', '')
        bun = jibun if '-' not in jibun else jibun[:jibun.index('-')]
        if bun == '가':
            continue
        ji = 0 if '-' not in jibun else jibun[jibun.index('-')+1:]
        linkerRTMS = LinkerRTMS.objects.filter(
            sggCode=sggCode,
            bjdName=bjd,
            bun=bun,
            ji=ji
        )
        if linkerRTMS.exists():
            if linkerRTMS.first().kaptCode is not None:
                RTMSRent.objects.create(
                    reality=Reality.objects.filter(kaptCode=linkerRTMS.first().kaptCode).first(),
                    amount=tree.find('보증금액').text.strip(),
                    rent=tree.find('월세금액').text.strip(),
                    year=tree.find('년').text.strip(),
                    month=tree.find('월').text.strip(),
                    day=tree.find('일').text.strip(),
                    useArea=tree.find('전용면적').text.strip(),
                    jibun=tree.find('지번').text.strip(),
                    floor=tree.find('층').text.strip(),
                )
        else:
            LinkerRTMS.objects.create(
                sggCode=sggCode,
                bjdName=bjd,
                bun=bun,
                ji=ji,
                kaptCode=None
            )
            reality = Reality.objects.filter(
                bjdCode__startswith=sggCode,
                secondName=bjd,
                bun=bun,
                ji=ji
            )
            if reality.exists():
                LinkerRTMS.objects.filter(
                    sggCode=sggCode,
                    bjdName=bjd,
                    bun=bun,
                    ji=ji,
                ).update(kaptCode = reality.first().kaptCode)
                RTMSRent.objects.create(
                    reality=Reality.objects.filter(kaptCode=linkerRTMS.first().kaptCode).first(),
                    amount=tree.find('보증금액').text.strip(),
                    rent=tree.find('월세금액').text.strip(),
                    year=tree.find('년').text.strip(),
                    month=tree.find('월').text.strip(),
                    day=tree.find('일').text.strip(),
                    useArea=tree.find('전용면적').text.strip(),
                    jibun=tree.find('지번').text.strip(),
                    floor=tree.find('층').text.strip(),
                )
    
    complete_rtms(dealYMD[:4], dealYMD[4:], sggCode)

def complete_rtms(y, m, sggCode):
    f = open('complete_rtmsrent.info', 'a')
    f.write('{0} {1} {2}\n'.format(y,m,sggCode))
    print("Complete: {0} {1} {2}".format(y,m,sggCode))
    f.close()
