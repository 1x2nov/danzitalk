from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User, Posting, PostingPrefer, Comment, CommentPrefer
from reality.models import Reality, Bookmark, RTMS, LinkerRTMS, RTMSRent
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from datetime import date, datetime, timedelta
import random
import json

def isLogin(request):
    if not request.user.is_authenticated:
        return None

    user_query = User.objects.filter(id=request.session.get('user_id', None))

    user = user_query.first()
    if user.nickname == '':
        s = ''.join([chr(random.randrange(44032, 55203+1)) for _ in range(3)])
        user_query.update(nickname=s)
    if user.profile_image == '':
        user_query.update(profile_image='default_profile.jpg')
    return user

class Join(APIView):
    def get(self, request):
        return render(request, "community/join.html")
    
    def post(self, request):
        nickname = request.data.get('nickname', None)
        name = request.data.get('name', None)
        email = request.data.get('email', None)
        password = request.data.get('password', None)

        User.objects.create(email=email, 
        nickname=nickname, 
        name=name, 
        password=make_password(password),
        profile_image="default_profile.jpg"
        )

        return Response(status=200)

class Login(APIView):
    def get(self, request):
        return render(request, "community/login.html")

    def post(self, request):
        email = request.data.get('email', None)
        password = request.data.get('password', None)

        user = User.objects.filter(email=email).first()

        if user is None:
            return Response(status=400, data=dict(message="회원정보가 잘못되었습니다."))

        if user.check_password(password):
            request.session['email'] = email
            return Response(status=200)
        
        else:
            return Response(status=400, data=dict(message="회원정보가 잘못되었습니다."))

class Profile(APIView):
    def get(self, request):
        user = isLogin(request)
        if user is None:
            return render(request, "community/login.html")

        bookmarks = Bookmark.objects.filter(user=user)
        
        reality_list = [
            {
            'reality':bookmark.reality, 
            'is_mark':True,
            'bookmark_count':bookmark.reality.bookmarks.count()
            } 
            for bookmark in bookmarks
        ]


        return render(request, "community/profile.html", context=dict(user=user, reality_list=reality_list))

class Logout(APIView):
    def get(self, request):
        request.session.flush()
        return render(request, "community/login.html")

class Board(APIView):
    def get(self, request, reality_id):
        reality = Reality.objects.filter(id=reality_id).first()

        user = isLogin(request)

        posting_list = []
        postings = Posting.objects.filter(reality__id=reality_id).order_by('-id')
        
        for posting in postings:

            likes = posting.prefers.filter(preference=1)
            hates = posting.prefers.filter(preference=-1)

            like_count = likes.count()
            hate_count = hates.count()

            is_like = likes.filter(user=user).exists()
            is_hate = hates.filter(user=user).exists()

            comment_count = posting.comments.count()

            posting_dict = {
                "posting":posting,
                "like_count":like_count,
                "hate_count":hate_count,
                "is_like":is_like,
                "is_hate":is_hate,
                "comment_count":comment_count
            }
            posting_list.append(posting_dict)

        is_mark = Bookmark.objects.filter(reality__id=reality_id, user=user).exists()

        dPcnt = reality.kaptdPcnt + reality.kaptdPcntu
        dpPdp = round(dPcnt / reality.kaptdaCnt, 2)
        
        s = reality.kaptTel
        kaptTel = '-'
        if s is not None:
            if len(s) == 9:
                i1, i2 = 2, 5
            elif len(s) == 10:
                i1, i2 = 3, 6
            elif len(s) == 11:
                i1, i2 = 3, 7
            kaptTel = "{}-{}-{}".format(s[:i1], s[i1:i2], s[i2:])

        rtmsQuery = RTMS.objects.filter(
            reality=reality
        ).extra(
            select={'yearint': 'CAST(year AS INTEGER)',
                'monthint': 'CAST(month AS INTEGER)',
                'dayint': 'CAST(day AS INTEGER)',
            }
        ).order_by('-yearint', '-monthint', '-dayint')

        rtmsAreaSet = set(rtms.useArea for rtms in rtmsQuery.all())

        rtmsDict = {}
        for rtmsArea in sorted(list(rtmsAreaSet)):
            rtmsDict[rtmsArea] = []
            for rtms in rtmsQuery.filter(useArea=rtmsArea).all():
                rtmsDict[rtmsArea].append({
                    'amount':rtms.amount,
                    'year':rtms.year,
                    'month':rtms.month,
                    'day':rtms.day,
                    'floor':rtms.floor,
                })

        
        rtmsRentQuery = RTMSRent.objects.filter(
            reality=reality
        ).extra(
            select={'yearint': 'CAST(year AS INTEGER)',
                'monthint': 'CAST(month AS INTEGER)',
                'dayint': 'CAST(day AS INTEGER)',
            }
        ).order_by('-yearint', '-monthint', '-dayint')

        rtmsRentAreaSet = set(rtmsRent.useArea for rtmsRent in rtmsRentQuery.all())

        rtmsRentDict = {}
        for rtmsRentArea in sorted(list(rtmsRentAreaSet)):
            rtmsRentDict[rtmsRentArea] = []
            for rtmsRent in rtmsRentQuery.filter(useArea=rtmsRentArea).all():
                rtmsRentDict[rtmsRentArea].append({
                    'amount':rtmsRent.amount,
                    'year':rtmsRent.year,
                    'month':rtmsRent.month,
                    'day':rtmsRent.day,
                    'floor':rtmsRent.floor,
                })

        response = render(request, "community/board.html", context=dict(user=user, 
            postings=posting_list, 
            reality_title=reality.secondName+" "+reality.kaptName, 
            reality_desc=reality.kaptAddr.replace(reality.kaptName, "").strip(),
            dPcnt = dPcnt,
            daPdp = dpPdp,
            kaptTel = kaptTel,
            reality=reality, 
            is_mark=is_mark,
            rtms_dict=rtmsDict,
            rtms_dict_json=json.dumps(rtmsDict),
            rtms_rent_dict=rtmsRentDict,
            rtms_rent_dict_json=json.dumps(rtmsRentDict),
            area_set = sorted(list(rtmsAreaSet)),
            ))

        expire_date, now = datetime.now(), datetime.now()
        expire_date += timedelta(hours=1)
        expire_date = expire_date.replace(minute=0, second=0, microsecond=0)
        expire_date -= now
        max_age = expire_date.total_seconds()

        cookie_value = request.COOKIES.get('hitboard', '_')
        
        if f'_{reality_id}_' not in cookie_value:
            cookie_value += f'_{reality_id}_'
            response.set_cookie('hitboard', value=cookie_value, max_age=max_age, httponly=True)
            reality.hits += 1
            reality.save()

        return response

class CreatePosting(APIView):
    def get(self, request, reality_id):

        user = isLogin(request)
        if user is None:
            return render(request, "community/login.html")

        return render(request, "community/create.html", context=dict(user=user, reality_id=reality_id))

    def post(self, request, reality_id):
        title = request.data.get('title', None)
        content = request.data.get('content', None)
        user_id = request.data.get('user_id', None)
        reality_id = request.data.get('reality_id', None)
        user = User.objects.filter(id=user_id).first()
        reality = Reality.objects.filter(id=reality_id).first()

        Posting.objects.create(title=title, 
        content=content,
        user=user,
        reality = reality
        )

        return Response(status=200)

class ReadPosting(APIView):
    def get(self, request, posting_id):
        context = {}

        user = isLogin(request)

        context['user'] = user

        posting = Posting.objects.filter(id=posting_id).first()
        context['posting'] = posting
        
        comments = posting.comments.all()
        context['comment_count'] = comments.count()
        context['comments'] = []
        for comment in comments:
            likes = comment.prefers.filter(preference=1)
            hates = comment.prefers.filter(preference=-1)

            like_count = likes.count()
            hate_count = hates.count()

            is_like = likes.filter(user=user).exists()
            is_hate = hates.filter(user=user).exists()

            comment_dict = {
                "comment":comment,
                "like_count":like_count,
                "hate_count":hate_count,
                "is_like":is_like,
                "is_hate":is_hate
            }
            context['comments'].append(comment_dict)

        prefers = posting.prefers.all()
        is_like = is_hate = False

        user_prefer = prefers.filter(user=user).first()

        if user_prefer is not None:
            if user_prefer.preference == 1: is_like = True
            else: is_hate = True

        context['is_like'] = is_like
        context['is_hate'] = is_hate

        likes = prefers.filter(preference=1)
        hates = prefers.filter(preference=-1)        
        like_count = likes.count()
        hate_count = hates.count()

        context['like_count'] = like_count
        context['hate_count'] = hate_count

        posting_list = []
        postings = Posting.objects.filter(reality__id=posting.reality.id).exclude(id=posting_id).order_by('-id')
        for item in postings:

            likes = item.prefers.filter(preference=1)
            hates = item.prefers.filter(preference=-1)

            like_count = likes.count()
            hate_count = hates.count()

            is_like = likes.filter(user=user).exists()
            is_hate = hates.filter(user=user).exists()

            comment_count = item.comments.count()

            posting_dict = {
                "posting":item,
                "like_count":like_count,
                "hate_count":hate_count,
                "is_like":is_like,
                "is_hate":is_hate,
                "comment_count":comment_count
            }
            posting_list.append(posting_dict)
        
        context['postings'] = posting_list

        expire_date, now = datetime.now(), datetime.now()
        expire_date += timedelta(days=1)
        expire_date = expire_date.replace(hour=0, minute=0, second=0, microsecond=0)
        expire_date -= now
        max_age = expire_date.total_seconds()

        cookie_value = request.COOKIES.get('hitposting', '_')

        response = render(request, "community/read.html", context=context)
        
        if f'_{posting_id}_' not in cookie_value:
            cookie_value += f'_{posting_id}_'
            response.set_cookie('hitposting', value=cookie_value, max_age=max_age, httponly=True)
            posting.hits += 1
            posting.save()

        return response

class CreateComment(APIView):
    def post(self, request, posting_id):
        content = request.data.get('content', None)
        user_id = request.data.get('user_id', None)
        user = User.objects.filter(id=user_id).first()
        posting = Posting.objects.filter(id=posting_id).first()
        Comment.objects.create(content=content, 
        posting=posting,
        user=user
        )

        return Response(status=200)

class TogglePostingLike(APIView):
    def post(self, request, posting_id):

        user_id = request.data.get('user_id', None)
        user = User.objects.filter(id=user_id).first()

        is_like = request.data.get('is_like', None)
        preference = 0 if is_like == 'true' else 1

        posting = Posting.objects.filter(id=posting_id).first()

        if preference == 0:
            PostingPrefer.objects.filter(user=user, posting=posting).delete()
        else:
            PostingPrefer.objects.create(
                preference=preference, 
                posting=posting,
                user=user
            )
        
        return Response(status=200)

class TogglePostingHate(APIView):
    def post(self, request, posting_id):

        user_id = request.data.get('user_id', None)
        user = User.objects.filter(id=user_id).first()

        is_hate = request.data.get('is_hate', None)
        preference = 0 if is_hate == 'true' else -1

        posting = Posting.objects.filter(id=posting_id).first()

        if preference == 0:
            PostingPrefer.objects.filter(user=user, posting=posting).delete()
        else:
            PostingPrefer.objects.create(
                preference=preference, 
                posting=posting,
                user=user
            )
        
        return Response(status=200)

class ToggleCommentLike(APIView):
    def post(self, request, comment_id):

        user_id = request.data.get('user_id', None)
        user = User.objects.filter(id=user_id).first()

        is_like = request.data.get('is_like', None)
        preference = 0 if is_like == 'true' else 1

        comment = Comment.objects.filter(id=comment_id).first()

        if preference == 0:
            CommentPrefer.objects.filter(user=user, comment=comment).delete()
        else:
            CommentPrefer.objects.create(
                preference=preference, 
                comment=comment,
                user=user
            )
        
        return Response(status=200)

class ToggleCommentHate(APIView):
    def post(self, request, comment_id):

        user_id = request.data.get('user_id', None)
        user = User.objects.filter(id=user_id).first()

        is_hate = request.data.get('is_hate', None)
        preference = 0 if is_hate == 'true' else -1

        comment = Comment.objects.filter(id=comment_id).first()

        if preference == 0:
            CommentPrefer.objects.filter(user=user, comment=comment).delete()
        else:
            CommentPrefer.objects.create(
                preference=preference, 
                comment=comment,
                user=user
            )
        
        return Response(status=200)

class DeletePosting(APIView):
    def post(self, request, posting_id):
        Posting.objects.filter(id=posting_id).delete()
        return Response(status=200)

class DeleteComment(APIView):
    def post(self, request, comment_id):
        Comment.objects.filter(id=comment_id).delete()
        return Response(status=200)

class UpdatePosting(APIView):
    def get(self, request, posting_id):

        user = isLogin(request)
        if user is None:
            return render(request, "community/login.html")

        return render(request, "community/update.html", context=dict(user=user, posting_id=posting_id))

    def post(self, request, posting_id):
        title = request.data.get('title', None)
        content = request.data.get('content', None)

        Posting.objects.filter(id=posting_id).update(title=title, 
        content=content
        )

        return Response(status=200)

class UpdateComment(APIView):
    def post(self, request, comment_id):
        content = request.data.get('content', None)

        Comment.objects.filter(id=comment_id).update(content=content)

        return Response(status=200)

class UpdateProfile(APIView):
    def post(self, request):
        user = isLogin(request)
        nickname = request.data.get('nickname', None)

        User.objects.filter(id=user.id).update(nickname=nickname)

        return Response(status=200)