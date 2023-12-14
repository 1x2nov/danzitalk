from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Reality, Bookmark
from django.db.models import Q
from community.models import User
from community.views import isLogin
from django.db.models import Count

class Search(APIView):
    def get(self, request):
        user = isLogin(request)

        search_text = request.session['search_text']
        search_text = '' if search_text is None else search_text.strip()
        is_none = True if len(search_text) == 0 else False

        search_text = search_text.replace("아파트", "").strip() if not is_none else ''
        realities = Reality.objects.filter(Q(kaptAddr__icontains=search_text)).distinct()[:10]

        marked_reality_list = False

        if not is_none and realities.exists():
            is_empty = False
            reality_list = [
                {
                'id':reality.id,
                'title':reality.secondName +" "+ reality.kaptName,
                'desc':reality.kaptAddr.replace(reality.kaptName, "").strip(),
                'is_mark':reality.bookmarks.filter(user=user).exists(),
                'bookmark_count':reality.bookmarks.count(),
                } 
                for reality in realities
            ]
            
        else:
            is_empty = True
            realities = Reality.objects.annotate(count=Count('bookmarks')).order_by('-hits', '-count')[:10]
            
            reality_list = [
                {
                'id':reality.id,
                'title':reality.secondName +" "+ reality.kaptName,
                'desc':reality.kaptAddr.replace(reality.kaptName, "").strip(),
                'is_mark':reality.bookmarks.filter(user=user).exists(),
                'bookmark_count':reality.bookmarks.count()
                } 
                for reality in realities
            ]

            bookmarks = Bookmark.objects.filter(user=user)
        
            marked_reality_list = [
                {
                'reality':bookmark.reality, 
                'is_mark':True,
                'bookmark_count':bookmark.reality.bookmarks.count()
                } 
                for bookmark in bookmarks
            ]
        
        return render(request, "reality/search.html", context=dict(marked_reality_list=marked_reality_list ,reality_list=reality_list, user=user, is_empty=is_empty, is_none=is_none))

class ToggleBookmark(APIView):
    def post(self, request, reality_id):
        user_id = request.data.get('user_id', None)
        is_mark = request.data.get('is_mark', None)=='true'

        if is_mark:
            Bookmark.objects.filter(user__id=user_id, reality__id=reality_id).delete()
        else:
            user = User.objects.filter(id=user_id).first()
            reality = Reality.objects.filter(id=reality_id).first()
            Bookmark.objects.create(user=user, reality=reality)


        return Response(status=200)