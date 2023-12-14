from community.models import User
from django.conf import settings
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    # 로그인후 사용자가 다음을 통해 성공적으로 인증한 직후에 호출
    def pre_social_login(self, request, sociallogin):         
        login = sociallogin.serialize()
        account   = login.get('account')
        self.request.session['user_id'] = account.get('user_id')
        extra_data = account.get('extra_data')
        self.request.session['user_uid'] = account.get('uid')        
        provider = account.get('provider')
        self.request.session['user_provider'] = provider

        user_name = user_profile_imag = ''
        if provider in  ('naver','google')  :
            user_name         = extra_data.get('email') or extra_data.get('name')            
            user_profile_imag = extra_data.get('profile_image') or extra_data.get('picture')
        elif provider == 'kakao':
            kakao_account     = extra_data.get('kakao_account')
            user_name         = kakao_account.get('email') or kakao_account.get('profile').get('nickname')            
            user_profile_imag = kakao_account.get('profile').get('thumbnail_image_url')

        if user_name != None:
            user_name = f'{user_name[:1]}**{user_name[3:]}'

        self.request.session['profile_image'] = user_profile_imag or 'https://res.cloudinary.com/dtfub5xym/image/upload/v1669638871/pb_comment_logo.png'
        self.request.session['user_name'] = user_name
        return settings.LOGIN_REDIRECT_URL

    # 로그인 전  사용자 인스턴스를 추가로 채우는 데 사용
    def populate_user(self, request, sociallogin, data):   

        return settings.LOGIN_REDIRECT_URL