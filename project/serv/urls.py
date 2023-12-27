from django.urls import path
# Импортируем созданное нами представление
from .views import PostsList, PostDetail, PostCreate, PostUpdate, PostDelete

urlpatterns = [
   path('', PostsList.as_view(), name='startpage'),
   path('<int:pk>', PostDetail.as_view(), name='detail'),
   path('create/', PostCreate.as_view(), name='create'),
   path('<int:pk>/update/', PostUpdate.as_view(), name='edit'),
   path('<int:pk>/delete/', PostDelete.as_view(), name='delete'),
]