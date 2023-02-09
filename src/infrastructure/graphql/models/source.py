from graphene import ObjectType, String


class Source(ObjectType):
    name = String(description="Source name")
