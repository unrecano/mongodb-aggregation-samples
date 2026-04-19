from typing import List, Dict, Any
from src.db import get_mongo_client
import pprint


def run_project_aggregation() -> List[Dict[str, Any]]:
    """
    Executes an aggregation pipeline using $project to format the output of grouped data.

    Returns:
        List[Dict[str, Any]]: A list of projected and formatted documents.
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
        {
            "$project": {
                "_id": 0,
                "Property Type": "$_id",
                "Cheaper": "$cheaper.price",
                "Expensive": "$expensive.price",
            }
        },
    ]

    with get_mongo_client() as client:
        collection = client["sample_airbnb"]["listingsAndReviews"]
        return list(collection.aggregate(pipeline))


if __name__ == "__main__":
    results = run_project_aggregation()
    for doc in results:
        pprint.pprint(doc)
