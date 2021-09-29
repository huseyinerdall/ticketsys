   
from django.urls import path
from .views import TicketDetail, TicketList, UserList, UserDetail, CategoryDetail, CategoryList,\
    AttachmentList, AddCommentToTicket, CommentList, SearchTicket, GetUserTickets
from django.conf.urls import include, url

app_name = 'api'

urlpatterns = [
    path('tickets', TicketList.as_view(), name='listtickets'),
    path('ticket/<int:pk>', TicketDetail.as_view(), name='oneticketinfo'),
    path('users/', UserList.as_view(), name='listusers'),
    path('user/<int:pk>/', UserDetail.as_view(), name='listusers'),
    path('categories/', CategoryList.as_view(), name='listusers'),
    path('category/<int:pk>/', CategoryDetail.as_view(), name='getcategory'),
    path('tickets/<str:label>/',SearchTicket.as_view()),
    path('user/<int:user>/tickets', GetUserTickets.as_view(), name='getuser\'sticket'),
    path('categories/', CategoryList.as_view(), name='listusers'),
    path('files/', AttachmentList.as_view(), name='getcategory'),
    path('comments/', CommentList.as_view(), name='getputcomment'),
    url(r'^ticket/add-comment/', AddCommentToTicket.as_view(), name='addcomment')
]