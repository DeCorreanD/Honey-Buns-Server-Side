from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import serializers, status
from honeybunsapi.models import Item, User, FavoriteItem, Order, OrderItem


class ItemView(ViewSet):
    """DjangoJuice Item View"""
    
    def retrieve(self, request, pk):
        """Handle GET Request for Single Item
        Returns:
            Response -- JSON Serialized Product
        """
        item = Item.objects.get(pk=pk)
        serializer = ItemSerializer(item)
        return Response(serializer.data)
      
    def list(self, request):

        item = Item.objects.all()
        user_id = request.query_params.get('userId', None)
        if user_id is not None:
            product = product.filter(user_id=user_id)
        serializer = ItemSerializer(item, many=True)
        item = Item.objects.all()
        uid = request.META['HTTP_AUTHORIZATION']
        user = User.objects.get(uid=uid)
        for items in item:
            items.favorited = len(FavoriteItem.objects.filter(user=user, product=items)) > 0
        serializer = ItemSerializer(item, many=True)
        return Response(serializer.data)
        

    def create(self, request):
        """Handle POST operations

        Returns
        Response -- JSON serialized Product instance
        """

        user_id = User.objects.get(pk=request.data["userId"])
        
        item = Item.objects.create(
            name=request.data["name"],
            description=request.data["description"],
            price=request.data["price"],
            image_url=request.data["imageUrl"],
            user_id=user_id,
        )
        serializer = ItemSerializer(item)
        return Response(serializer.data)
    
    def update(self, request, pk):
        """Handle PUT requests for a product

        Returns:
        Response -- Empty body with 204 status code
        """

        item = Item.objects.get(pk=pk)
        item.name = request.data["name"]
        item.description = request.data["description"]
        item.image_url = request.data["imageUrl"]
        item.price = request.data["price"]
        item.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk):
        """Delete Product
        """
        item = Item.objects.get(pk=pk)
        item.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
     
    @action(detail=True, methods=['post'])
    def favorite(self, request, pk=None):
        """Favorite a item."""
        product = Item.objects.get(pk=pk)
        user = User.objects.get(uid=request.META["HTTP_AUTHORIZATION"])


        favorited = FavoriteItem.objects.create(product=product, user=user)
        return Response({'message': 'item favorited successfully!'}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['delete'])
    def unfavorite(self, request, pk=None):
        """Unfavorite a item."""
        product = Item.objects.get(pk=pk)
        user = User.objects.get(uid=request.META["HTTP_AUTHORIZATION"])
        print(product, user)

        favorited = FavoriteItem.objects.get(product=product, user=user)

        favorited.delete()
        return Response({'message': 'item unfavorited successfully!'}, status=status.HTTP_204_NO_CONTENT)
class ItemSerializer(serializers.ModelSerializer):
    """JSON Serializer For Item"""
    class Meta:
        model = Item
        fields = ('id', 'name', 'description', 'image_url', 'price', 'user_id', 'favorited')
        depth = 1
