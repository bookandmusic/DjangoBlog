from django.urls import path

from blog import views

app_name = 'blog'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('pages/<int:page_number>/', views.PageView.as_view(), name='page'),
    path('post/<int:pk>/', views.PostView.as_view(), name='post'),
    path('archives/<int:page_number>/', views.ArchivesView.as_view(), name='archive'),
    path('archives/<int:year>/<int:month>/<int:page_number>/', views.ArchivesYearMonthView.as_view(),
         name='archive_year_month'),

    path('tags/', views.TagView.as_view(), name='tags'),
    path('tag/<int:pk>/<int:page_number>/', views.TagPostView.as_view(), name='tag_post'),

    path('tutorial/<int:page_number>/', views.TutorialsView.as_view(), name='tutorials'),
    path('tutorial/<int:pk>/<int:page_number>/', views.TutorialPostView.as_view(), name='tutorial_post'),
    path('search/', views.KeyWordSearch(), name='haystack_search'),
    path('add_post/', views.AddPostView.as_view(), name='add_post'),
]
