from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from honeybunsapi.models import FavoriteItem, User
from honeybunsapi.views.item import ItemSerializer

class FavoriteItemView(ViewSet):
    """Honey Buns View"""
    def retrieve(self, request, pk):
        """GET request for a single user"""
        try:
            favorite_item = FavoriteItem.objects.get(pk=pk)
            serializer = FavoriteItemSerializer(favorite_item)
            return Response(serializer.data)
        except FavoriteItem.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """GET request for a list of users"""
        favorite_items = FavoriteItem.objects.all()
        uid = request.META['HTTP_AUTHORIZATION']
        user = User.objects.get(uid=uid)
        favorite_items = favorite_items.filter(user_id = user)
        serializer = FavoriteItemSerializer(favorite_items, many=True, context={'request': request})
        return Response(serializer.data)
    
class FavoriteItemSerializer(serializers.ModelSerializer):
  """JSON serializer for categories"""
#   item = ItemSerializer()
  class Meta:
      model = FavoriteItem
      fields = ('id', 'product', 'user')
      depth = 1
