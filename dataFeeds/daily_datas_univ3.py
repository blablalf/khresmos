from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

# use this playground for testing
# https://thegraph.com/hosted-service/subgraph/uniswap/uniswap-v3

def fetch_uniswap_data():
    transport=RequestsHTTPTransport(
        url='https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3',
        verify=True,
        retries=5,
    )
    client = Client(
        transport=transport,
        fetch_schema_from_transport=True,
    )

    query = gql("""
        {
            pool(id:"0xd1d8dfa3012888f752478b49a9700907362b807e") {
            id
            token0 {
                symbol
            }
            token1 {
                symbol
            }
                sqrtPrice
                liquidity
            }
        }

    """)

    response = client.execute(query)
    print(response)

fetch_uniswap_data()
