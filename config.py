import os
from falkordb import FalkorDB

# FalkorDB Cloud Connection Settings
FALKOR_HOST = os.getenv("FALKOR_HOST", "r-6jissuruar.instance-ybo5wil4l.hc-7up0crkyn.ap-south-1.aws.f2e0a955bb84.cloud")
FALKOR_PORT = int(os.getenv("FALKOR_PORT", 59882))
FALKOR_USERNAME = os.getenv("FALKOR_USERNAME", "falkordb")
FALKOR_PASSWORD = os.getenv("FALKOR_PASSWORD", "LlSYoKQQIN69")
GRAPH_NAME = "BreachPath_Security_Graph"

def get_graph():
    """Connect to FalkorDB Cloud instance and return the graph."""
    # Cloud instances typically communicate over standard TCP or SSL
    try:
        db = FalkorDB(
            host=FALKOR_HOST,
            port=FALKOR_PORT,
            username=FALKOR_USERNAME,
            password=FALKOR_PASSWORD,
            ssl=False
        )
        return db.select_graph(GRAPH_NAME)
    except Exception as e:
        # Fallback to SSL=True if required by cloud provider
        db = FalkorDB(
            host=FALKOR_HOST,
            port=FALKOR_PORT,
            username=FALKOR_USERNAME,
            password=FALKOR_PASSWORD,
            ssl=True
        )
        return db.select_graph(GRAPH_NAME)
