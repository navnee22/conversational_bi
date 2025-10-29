import requests
import os

MCP_URL = os.getenv("MCP_URL")

def get_table_metadata(data_source: str):
    """Fetch table schema and sample data from Tableau MCP."""
    payload = {"data_source": data_source}
    response = requests.post(f"{MCP_URL}/metadata", json=payload)
    response.raise_for_status()
    return response.json()
