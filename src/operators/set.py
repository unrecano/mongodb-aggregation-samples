from typing import List, Dict, Any
from src.db import get_mongo_client
import pprint

def run_set_aggregation() -> List[Dict[str, Any]]:
    """
    Executes an aggregation pipeline using $set to add calculated fields and restructure documents.

    Returns:
        List[Dict[str, Any]]: A list of aggregated and restructured documents.
    """
    pipeline = [
        {"$match": {"address.country_code": "US"}},
        {"$sort": {"property_type": 1, "price": 1}},
        {
            "$group": {
                "_id": "$property_type",
                "count": {"$sum": 1},
                "average": {"$avg": "$price"},
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
            "$set": {
                "Property Type": "$_id",
                "Amount of properties": "$count",
                "Average Price": {"$round": ["$average", 2]},
                "Properties": [
                    {
                        "Type": "Cheaper",
                        "Name": "$cheaper.name",
                        "Price": "$cheaper.price",
                    },
                    {
                        "Type": "Expensive",
                        "Name": "$expensive.name",
                        "Price": "$expensive.price",
                    },
                ],
            }
        },
        {
            "$project": {
                "_id": 0,
                "count": 0,
                "average": 0,
                "cheaper": 0,
                "expensive": 0,
            }
        },
    ]

    with get_mongo_client() as client:
        collection = client["sample_airbnb"]["listingsAndReviews"]
        return list(collection.aggregate(pipeline))

if __name__ == "__main__":
    results = run_set_aggregation()
    for doc in results:
        pprint.pprint(doc)
