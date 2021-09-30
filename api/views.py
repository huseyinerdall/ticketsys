from rest_framework import generics, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from app.models import Ticket, User, Category, Attachment, Comment
from .serializers import TicketSerializer, UserSerializer, CategorySerializer, AttachmentSerializer, CommentSerializer
from django.shortcuts import get_object_or_404
from rest_framework.parsers import JSONParser
import json
import datetime
today = datetime.datetime.today()
from django.utils.datastructures import MultiValueDictKeyError

class TicketList(generics.ListCreateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

class TicketDetail(generics.RetrieveDestroyAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryDetail(generics.RetrieveDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class AttachmentList(generics.ListCreateAPIView):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer

class CommentList(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class AddCommentToTicket(APIView):

    def post(self, request):
        comment = request.POST['comment']
        pk = request.POST['pk']
        user = request.POST['user']
        attachments = request.POST['attachments']

        t = get_object_or_404(Ticket, pk=pk)

        u = User(pk=user)
        attachments_objects = []
        attachments_ids = []
        a = None
        for id in attachments.split(','):
            attachments_objects.append(Attachment.objects.get(pk=id))
            attachments_ids.append(id)
            print(Attachment.objects.get(pk=id))
            a = Attachment.objects.get(pk=id)
        c = Comment.objects.create(comment=comment, created_at=today.isoformat(), user=u)
        c.attachments.set(attachments_objects)
        #print(attachments_objects)
        #print(*attachments_objects)
        #c.attachments.set(37)


        t.comments.add(c)





        # if no model exists by this PK, raise a 404 error

        # this is the only field we want to update
        #t.comments.add(c)
        #existcomments = json.loads(model.comments)
        #existcomments.append({"comment": comment,"created_at":created_at,"user":user,"ticket":pk})
        #data = {"comments": json.dumps(existcomments)}
        #serializer = TicketSerializer(model, data=data, partial=True)
        #print(serializer.is_valid())
        #if serializer.is_valid():
        #    serializer.save()
        #    return Response(serializer.data)
        # return a meaningful error response
        return Response('serializer.errors')

class SearchTicket(APIView):

    def get(self, request, label):
        model = Ticket.label_search(Ticket, search=label)
        return Response(model.values())

class GetUserTickets(APIView):

    def get(self, request, user):
        model = Ticket.get_user_tickets(Ticket, user=user)
        return Response(model.values())

""" Concrete View Classes
#CreateAPIView
Used for create-only endpoints.
#ListAPIView
Used for read-only endpoints to represent a collection of model instances.
#RetrieveAPIView
Used for read-only endpoints to represent a single model instance.
#DestroyAPIView
Used for delete-only endpoints for a single model instance.
#UpdateAPIView
Used for update-only endpoints for a single model instance.
##ListCreateAPIView
Used for read-write endpoints to represent a collection of model instances.
RetrieveUpdateAPIView
Used for read or update endpoints to represent a single model instance.
#RetrieveDestroyAPIView
Used for read or delete endpoints to represent a single model instance.
#RetrieveUpdateDestroyAPIView
Used for read-write-delete endpoints to represent a single model instance.
"""