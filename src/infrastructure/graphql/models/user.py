from graphene import ObjectType, String


class User(ObjectType):
    email = String(description="User email")
