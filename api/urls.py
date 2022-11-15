from django.urls import path
from api import views
# from api.views import NoteListView, NoteDetailView
from api.views import NoteViewSet
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter

app_name = 'api'

router = DefaultRouter()
router.register('notes', NoteViewSet, basename='notes')  # basename - то, что до - в urlpatterns
urlpatterns = router.urls

# notes_list = NoteViewSet.as_view({
#     'get': 'list',
#     'post': 'create'
# })
#
# notes_detail = NoteViewSet.as_view({
#     'get': 'retrieve',
#     'put': 'update',
#     'patch': 'partial_update',
#     'delete': 'destroy'
# })
#
# urlpatterns = [
#     path('notes/', notes_list, name='notes-list'),
#     path('notes/<int:pk>/', notes_detail, name='notes-detail'),
# ]

# urlpatterns = format_suffix_patterns(urlpatterns)
