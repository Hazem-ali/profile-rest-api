from rest_framework import authentication
from rest_framework.decorators import authentication_classes
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework import status  # HTTP STATUSES
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication

# Login Authentication imports
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

# is auth or read only
from rest_framework.permissions import IsAuthenticated


# to be able to search well
from rest_framework import filters

from profiles_api import serializers, models
from profiles_api import permissions


class HelloAPIView(APIView):

    # guarantees the form of data inside
    serializer_class = serializers.HelloSerializer

    def get(self, request, format=None):
        'returns a list or dict contains data'
        an_apiview = [
            'mofty',
            'hazem',
            'zooma',
            'zoooomzom'
        ]

        return Response({'message': 'Hello', 'an_apiview': an_apiview})

    def post(self, request):
        """Create a hello msg with our name"""

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}'
            return Response({'message': message})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def put(self, request, pk=None):
        """Updates an object by replacing"""

        return Response({'Method': "PUT"})

    def patch(self, request, pk=None):
        """Updates an object partially"""

        return Response({'Method': "PATCH"})

    def delete(self, request, pk=None):
        """Delete an object """

        return Response({'Method': "DELETE"})


class HelloViewSet(viewsets.ViewSet):
    """ test viewset """
    serializer_class = serializers.HelloSerializer

    def list(self, request):
        """return a hello message"""
        a_viewset = [
            'this viewset1',
            'this viewset2',
            'this viewset3'
        ]

        return Response({'message': 'Helloooo', 'a_viewset': a_viewset})

    def create(self, request):
        """ creates a new hello msg"""

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hellooooooooooo {name}'
            return Response({'message': message})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def retrieve(self, request, pk=None):

        return Response({'http_method': 'GET'})

    def update(self, request, pk=None):

        return Response({'http_method': 'PUT'})

    def partial_update(self, request, pk=None):
        # patch
        return Response({'http_method': 'PATCH'})

    def destroy(self, request, pk=None):
        # delete
        return Response({'http_method': 'DELETE'})


class UserProfileViewSet(viewsets.ModelViewSet):
    """Handle creating and updating profiles"""

    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()

    # authentication
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)

    # searching
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email',)


class UserLoginApiView(ObtainAuthToken):
    """handle creating auth tokens for user"""

    # ADD renderer to obtainauthtoken to be able to view it
    # it existed by default in modelviewset but not here
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """handles create, read and update profile feed items"""

    # authentication
    authentication_classes = (TokenAuthentication,)

    serializer_class = serializers.ProfileFeedItemSerializer
    queryset = models.ProfileFeedItem.objects.all()

    permission_classes = (
        permissions.UpdateOwnProfile,
        IsAuthenticated)

    def perform_create(self, serializer):
        "sets the user profile to the logged in user"
        # save the content to database
        serializer.save(user_profile=self.request.user)

