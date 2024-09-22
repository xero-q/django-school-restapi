import graphene
from graphene_django.types import DjangoObjectType
from .models import PersonModel

class PersonModelType(DjangoObjectType):
    class Meta:
        model = PersonModel

class Query(graphene.ObjectType):
    list_people = graphene.List(
        PersonModelType,
        sex=graphene.String(required=False)  # Add an argument for filtering by sex
    )

    def resolve_list_people(root, info, sex=None):
        if sex:
            return PersonModel.objects.filter(sex=sex)
        return PersonModel.objects.all()

schema = graphene.Schema(query=Query)
