from graphene import ObjectType, String, Boolean

from infrastructure.graphql.custom_date_time import CustomDateTime


class NewDetail(ObjectType):
    content = String(description="New full content")
    date = CustomDateTime(description="New publish date and time")
    hydrated = Boolean(description="True if the new has been hydrated with the NLP data, false otherwise")
    summary = String(description="New content summary")
