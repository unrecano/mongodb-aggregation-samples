from typing import List, Dict, Any
from src.db import get_mongo_client
import pprint

def run_group_aggregation() -> List[Dict[str, Any]]:
    """
    Executes an aggregation pipeline using $group to get the cheapest and most expensive property by type.

    Returns:
        List[Dict[str, Any]]: A list of aggregated documents grouped by property type.
    """
    pipeline = [
        {"$match": {"address.country_code": "US"}},
        {"$sort": {"property_type": 1, "price": 1}},
        {
            "$group": {
                "_id": "$property_type",
                "cheaper": {
                    "$first": {
                        "name": "$name",
                        "price": "$price",
                        "address": "$address",
                    }
                },
                "expensive": {
                    "$last": {"name": "$name", "price": "$price", "address": "$address"}
                },
            }
        },
    ]

    with get_mongo_client() as client:
        collection = client["sample_airbnb"]["listingsAndReviews"]
        return list(collection.aggregate(pipeline))

if __name__ == "__main__":
    results = run_group_aggregation()
    for doc in results:
        pprint.pprint(doc)
