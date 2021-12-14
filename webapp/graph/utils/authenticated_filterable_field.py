from aiohttp.web_exceptions import HTTPUnauthorized
from graphene_sqlalchemy_filter import FilterableConnectionField


class AuthenticatedFilterableField(FilterableConnectionField):
    @classmethod
    def resolve_connection(cls, connection_type, model, info, args, resolved):
        request = info.context["request"]
        if not request.user:
            raise HTTPUnauthorized(reason="User is not present")
        return super().resolve_connection(connection_type, model, info, args, resolved)
