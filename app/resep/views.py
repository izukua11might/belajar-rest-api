from rest_framework.authentication import TokenAuthentication
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from core.models import Tag, Ingredient, Recipe

from resep import serializers


class BaseResipeAttrViewset(viewsets.GenericViewSet,
                            mixins.ListModelMixin,
                            mixins.CreateModelMixin):

    """viewsets dasar untuk authenticate dan perizinan"""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """mengembalikan objects pada pengguna yang di otentikasi saja"""
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """membuat bahan baru"""
        serializer.save(user=self.request.user)

class TagViewSet(BaseResipeAttrViewset):
    """mengatur tags api di database"""
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer

class IngredientViewSet(BaseResipeAttrViewset):
    """Manage ingredients in the database"""
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer

class RecipeViewSet(viewsets.ModelViewSet):
    """mengatur recipe api dalam database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes =  (IsAuthenticated,)
    queryset = Recipe.objects.all()
    serializer_class = serializers.RecipeSerializer

    def get_queryset(self):
        """return object pada user ter authentikasi"""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        """return serializer class yang sesuai"""
        if self.action == 'retrieve':
            return serializers.RecipeDetailSerializer

        return self.serializer_class
