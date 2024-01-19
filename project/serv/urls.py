from django.urls import path
from .views import PostsList, PostDetail, PostCreate, PostUpdate, PostDelete, \
   PostSearch, CommentList, CommentDetail, CommentDelete, CommentUpdate, CommentCreate
from .views import upgrade_me

urlpatterns = [
   path('', PostsList.as_view(), name='startpage'),
   path('<int:pk>', PostDetail.as_view(), name='detail'),
   path('create/', PostCreate.as_view(), name='create'),
   path('<int:pk>/update/', PostUpdate.as_view(), name='edit'),
   path('<int:pk>/delete/', PostDelete.as_view(), name='delete'),
   path('upgrade/', upgrade_me, name='upgrade'),
   path('search/', PostSearch.as_view),
   path('comments/', CommentList.as_view(), name="comment_list"),
   path('comments/create', CommentCreate.as_view(), name="comment_create"),
   path('comments/<int:pk>/', CommentDetail.as_view(), name="comment_detail"),
   path('<int:pk>/update/', CommentUpdate.as_view(), name='comment_update'),
   path('<int:pk>/delete/', CommentDelete.as_view(), name='comment_delete'),
]