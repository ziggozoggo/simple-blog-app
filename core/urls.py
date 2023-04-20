from django.urls import path
from . import views

app_name = 'core'
urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('create/', views.create_post, name='post_create'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>', views.post_detail, name='post_detail'),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    path('<int:post_id>/comment/', views.post_comment, name='post_comment'),
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
]
