"""
News Manager service interface module
"""
from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport

from log_config import get_logger

LOGGER = get_logger()


GET_NEW_BY_TITLE_QUERY = gql('''
    query getNewByTitle($title: String) {
        new(title: $title){
            title
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
        }
    }
''')


class NewsManagerService:
    """
    News manager service interface implementation
    """
    GQL_URL = '{protocol}://{host}:{port}/graphql'

    def __init__(self, protocol: str, host: str, port: str):
        """
        Initialize the news manager service interface creating the gql client

        Args:
            protocol: news manager service communications protocol
            host: news manager service host IP address
            port: news manager service port
        """
        gql_url = NewsManagerService.GQL_URL.format(protocol=protocol, host=host, port=port)
        transport = RequestsHTTPTransport(url=gql_url, use_json=True,
                                          headers={"Content-type": "application/json", }, verify=False, retries=3)
        self._gql_client = Client(transport=transport, fetch_schema_from_transport=True)

    async def get_new_by_title(self, title: str) -> dict:
        """
        Get the new identified by the given title

        Args:
            title: title of the new to get

        Returns: new identified by the specified title

        """
        LOGGER.info(f'Requesting the new {title} to the news manager')
        return self._gql_client.execute(GET_NEW_BY_TITLE_QUERY, title=title)
