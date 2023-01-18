from graphene import ObjectType, String


class NamedEntityType(ObjectType):
    name = String(description="Named entity name")
    description = String(description="Named entity description")
