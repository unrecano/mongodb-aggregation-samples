from typing import List, Dict, Any
from src.db import get_mongo_client
import pprint

def run_lookup_aggregation() -> List[Dict[str, Any]]:
    """
    Executes an aggregation pipeline using $lookup to join data between customers, accounts, and transactions.

    Returns:
        List[Dict[str, Any]]: A list of aggregated documents containing the joined data.
    """
    pipeline = [
        {
            "$lookup": {
                "from": "accounts",
                "localField": "accounts",
                "foreignField": "account_id",
                "as": "account_info",
            }
        },
        {"$unwind": "$account_info"},
        {
            "$lookup": {
                "from": "transactions",
                "localField": "account_info.account_id",
                "foreignField": "account_id",
                "as": "account_transactions",
            }
        },
        {"$unwind": "$account_transactions"},
        {
            "$group": {
                "_id": "$name",
                "total": {"$sum": {"$size": "$account_transactions.transactions"}},
            }
        },
        {"$sort": {"total": -1}},
        {"$limit": 5},
        {"$project": {"_id": 0, "Name": "$_id", "total": 1}},
    ]

    with get_mongo_client() as client:
        collection = client["sample_analytics"]["customers"]
        return list(collection.aggregate(pipeline))

if __name__ == "__main__":
    results = run_lookup_aggregation()
    pprint.pprint(results)
