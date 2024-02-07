from django.urls import path

from men import views

app_name = 'men'

urlpatterns = [
    path('home/', views.HomePageView.as_view(), name='home'),
    path('create-post/', views.CreateFormView.as_view(), name='post_create'),
    path('communicate/', views.SendEmailPageView.as_view(), name='communicate'),
    path('about-site/', views.AboutSitePageView.as_view(), name='about-site'),
    path('search/', views.SearchListView.as_view(), name='search'),
    path('detail/<slug:post_slug>/', views.DetailPageView.as_view(), name='post_detail'),
    path('category/<slug:cat_slug>/', views.CatPageList.as_view(), name='category'),
    path('tags/<slug:tag_slug>/', views.TagPageList.as_view(), name='tag'),
]