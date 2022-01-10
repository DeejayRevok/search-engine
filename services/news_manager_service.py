from logging import Logger

from jwt import encode
from typing import ClassVar

from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport


class NewsManagerService:
    __JWT_AUTH_ALGORITHM: ClassVar[str] = "HS256"
    __GQL_URL_PATTERN: ClassVar[str] = "{protocol}://{host}:{port}/graphql"
    __GET_NEW_BY_TITLE_QUERY: ClassVar[gql] = gql(
        """
        query getNewByTitle($searchTitle: String!) {
            new(title: $searchTitle){
                title
                url
                content
                source
                date
                hydrated
                entities {
                  text
                  type
                }
                summary
                sentiment
                nounChunks
            }
        }
    """
    )

    def __init__(self, protocol: str, host: str, port: str, jwt_secret: str, logger: Logger):
        self.__gql_url = self.__GQL_URL_PATTERN.format(protocol=protocol, host=host, port=port)
        self.__gql_client = None
        self.__logger = logger
        self.__jwt_secret = jwt_secret

    async def get_new_by_title(self, title: str) -> dict:
        self.__logger.info("Requesting the new %s to the news manager", title)
        self.__initialize()
        return self.__gql_client.execute(self.__GET_NEW_BY_TITLE_QUERY, variable_values=dict(searchTitle=title))["new"]

    def __initialize(self):
        if self.__gql_client is None:
            transport = RequestsHTTPTransport(
                url=self.__gql_url,
                use_json=True,
                headers={"Content-type": "application/json", "X-API-Key": "Bearer " + self.__generate_auth_token()},
                verify=False,
                retries=3,
            )
            self.__gql_client = Client(transport=transport, fetch_schema_from_transport=True)

    def __generate_auth_token(self) -> str:
        return encode(dict(user_id=-1000), key=self.__jwt_secret, algorithm=self.__JWT_AUTH_ALGORITHM).decode("utf-8")
