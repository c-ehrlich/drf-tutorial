from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from rest_framework import generics, permissions, renderers, viewsets
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.contrib.auth.models import User
from snippets.serializers import UserSerializer
from snippets.permissions import IsOwnerOrReadOnly


class SnippetViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve,
    `update` and `destroy` actions.
    
    Additionally we also provide an extra `highlight` action.
    
    It replaces the SnippetList, SnippetDetail, and SnippetHighlight classes
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    # the @action decorator can be used to add any custom endpoints that don't fit into the standard
    # create/update/delete style.
    # Custom actions which use the @action decorator will respond to GET requests by default. We can use the
    # `methods` argument if we wanted an action that responded to POST requests.
    # The URLs for custom actions by default depend on the method name itself. If you want to change the way the url
    # should be constructed, you can include `url_path` as a decorator keyword argument.
    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs): # this is the same as the get() function from SnippetHighlight
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer): # override the save function to include user information for each snippet
        serializer.save(owner=self.request.user)
# class SnippetList(generics.ListCreateAPIView):
#     """
#     List all code snippets, or create a new snippet
#     """
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#     def perform_create(self, serializer): # override the save function to include user information for each snippet
#         serializer.save(owner=self.request.user)
# class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
#     """
#     Retrief, update, or delete a code snippet.
#     """
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly,
#                           IsOwnerOrReadOnly]
# class SnippetHighlight(generics.GenericAPIView):
#     queryset = Snippet.objects.all()
#     renderer_classes = [renderers.StaticHTMLRenderer]

#     def get(self, request, *args, **kwargs):
#         snippet = self.get_object()
#         return Response(snippet.highlighted)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provieds `list` and `retrieve` actions.
    It replaces the UserList and UserDetail classes
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
# class UserList(generics.ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
# class UserDetail(generics.RetrieveAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format),
    })


