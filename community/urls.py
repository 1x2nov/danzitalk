from django.urls import path
from community import views
from .views import Join, Login, Profile, Logout, Board, CreatePosting, ReadPosting, CreateComment, TogglePostingLike, TogglePostingHate, ToggleCommentLike, ToggleCommentHate, DeletePosting, DeleteComment, UpdatePosting, UpdateComment, UpdateProfile

urlpatterns = [
    path('<int:reality_id>', Board.as_view(), name="board"),
    path('join', Join.as_view()),
    path('login', Login.as_view()),
    path('profile', Profile.as_view()),
    path('logout', Logout.as_view()),
    path('<int:reality_id>/create', CreatePosting.as_view(), name="create_posting"),
    path('read/<int:posting_id>', ReadPosting.as_view()),
    path('create/<int:posting_id>', CreateComment.as_view()),
    path('like/<int:posting_id>', TogglePostingLike.as_view()),
    path('hate/<int:posting_id>', TogglePostingHate.as_view()),
    path('comment/like/<int:comment_id>', ToggleCommentLike.as_view()),
    path('comment/hate/<int:comment_id>', ToggleCommentHate.as_view()),
    path('delete/<int:posting_id>', DeletePosting.as_view(), name="delete_posting"),
    path('comment/delete/<int:comment_id>', DeleteComment.as_view(), name="delete_comment"),
    path('update/<int:posting_id>', UpdatePosting.as_view()),
    path('comment/update/<int:comment_id>', UpdateComment.as_view()),
    path('profile/update', UpdateProfile.as_view()),
]