from graphene import ObjectType

from infrastructure.graphql.mutations.newspaper.create_newspaper_mutation import CreateNewspaperMutation
from infrastructure.graphql.mutations.newspaper.delete_newspaper_mutation import DeleteNewspaperMutation
from infrastructure.graphql.mutations.newspaper.update_newspaper_mutation import UpdateNewspaperMutation


class NewspaperMutations(ObjectType):
    create_newspaper = CreateNewspaperMutation.Field()
    update_newspaper = UpdateNewspaperMutation.Field()
    delete_newspaper = DeleteNewspaperMutation.Field()
