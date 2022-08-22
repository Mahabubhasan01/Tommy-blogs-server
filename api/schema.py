import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth.models import User


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = '__all__'


class Query(graphene.ObjectType):
    """
    Queries for the Restaurant model
    """
    user = graphene.List(UserType)

    def resolve_user(self, info, **kwargs):
        return User.objects.all()


class CreateUser(graphene.Mutation):
    class Arguments:
        username = graphene.String()
        first_name = graphene.String()
        last_name = graphene.String()
        email = graphene.String()
        password = graphene.String()
    user = graphene.Field(UserType)

    def mutate(self, info, username, first_name, last_name, email, password):
        user = User(username=username, first_name=first_name,
                    last_name=last_name, email=email, password=password)
        user.save()
        return CreateUser(user=user)


class UpdateUser(graphene.Mutation):
    class Arguments:
        id = graphene.Int()
        username = graphene.String()
        first_name = graphene.String()
        last_name = graphene.String()
        email = graphene.String()
        password = graphene.String()

    user = graphene.Field(UserType)

    def mutate(self, info, id, username, first_name, last_name, email, password):
        user = User.objects.get(id=id)
        user.username = username,
        user.first_name = first_name,
        user.last_name = last_name,
        user.email = email,
        user.password = password
        user.save()
        return UpdateUser(user=user)


""" class DeleteUser(graphene.Mutation):
    class Arguments:
        id = graphene.Int()

    def mutate(self, id, info):
        user = User.objects.get(id=id)
        user.delete()
        return DeleteUser() """


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    # delete_user = DeleteUser.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
