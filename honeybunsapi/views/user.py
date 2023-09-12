from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from honeybunsapi.models import User


class UserView(ViewSet):
  """Honeybuns API User View"""

  def list(self, request):
    """Handle GET requests for users
    
    Returns 
      Response -- JSON serialized list of users
    """
    
    # get all users 
    users = User.objects.all()
    
    # Establish the query parameter of uid and 
    # use the .get method to retrieve the object with matching 
    # uid value. If no user is found, an exception is raised.
    uid = request.query_params.get('uid')
    
    # if the uid exists, filter the list of users by the uid
    if uid:
        users = users.filter(uid=uid)
    
    # serialize any matching instances
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)
  
  
  def retrieve(self, request, pk):
    """Handle GET request for a single user
    
    Returns -- JSON serialized user object
    """
    
    try:
        user = User.objects.get(pk=pk)
        
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
      
    except User.DoesNotExist as ex:
      return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND) 
    
  def update(self, request, pk):
        """PUT request to update a user"""
        user = User.objects.get(pk=pk)
        
        user.first_name = request.data['firstName']
        user.last_name = request.data['lastName']
        user.email = request.data['email']
        user.phone_number = request.data['phoneNumber']
        user.address = request.data['address']
      
        user.save()
        return Response({'message': 'User UPDATED'}, status=status.HTTP_204_NO_CONTENT)

  def destroy(self, request, pk):
        """DELETE request to delete a user"""
        user = User.objects.get(pk=pk)
        user.delete()
        return Response({'message': 'User DESTROYED'}, status=status.HTTP_204_NO_CONTENT)    

class UserSerializer(serializers.ModelSerializer):
      """JSON serializer for rare_users"""
      
      class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'phone_number', 'email', 'address', 'uid')
        depth = 1
          
    
