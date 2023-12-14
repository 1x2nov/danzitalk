from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from community.models import User
from community.views import isLogin
from reality.models import Reality, RTMS
import json

def convert_number_string(number_string):
    number = int(number_string.replace(",", ""))
    number_string = str(number/10000)
    length = len(number_string)
    return number_string + "억"

class Main(APIView):
    def get(self, request):

        user = isLogin(request)

        realities = Reality.objects.exclude(x=0.0,y=0.0).all()
        marker_coor = []

        for reality in realities:
            '''
            rtms = RTMS.objects.filter(
                reality=reality
            ).extra(
                select={'yearint': 'CAST(year AS INTEGER)',
                    'monthint': 'CAST(month AS INTEGER)',
                    'dayint': 'CAST(day AS INTEGER)',
                }
            ).order_by('-yearint', '-monthint', '-dayint').first()
            '''

            marker_coor.append({
                'x':reality.x,
                'y':reality.y,
                'id':reality.id,
                'name':reality.kaptName,
                'address':reality.kaptAddr,
                #'amount':convert_number_string(rtms.amount) if rtms is not None else '-',
                #'area':str(int(rtms.useArea))+'㎡' if rtms is not None else '-',
            })

        return render(request, "danzitalk/main.html", context=dict(user=user, realities=json.dumps(marker_coor)))

    def post(self, request):
        search_text = request.data.get('search_text', None)
        
        request.session['search_text'] = search_text
        return Response(status=200)
        