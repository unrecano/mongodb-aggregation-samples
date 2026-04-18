from typing import List, Dict, Any
from src.db import get_mongo_client
import pprint

def run_unwind_aggregation() -> List[Dict[str, Any]]:
    """
    Executes an aggregation pipeline using $unwind to deconstruct arrays (amenities) and group by each element.

    Returns:
        List[Dict[str, Any]]: A list of aggregated documents grouped by the unwound array elements.
    """
    pipeline = [
        {"$unwind": "$amenities"},
        {"$group": {"_id": "$amenities", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10},
        {
            "$project": {
                "_id": 0,
                "Amenity": "$_id",
                "Amount": "$count",
                "Percentage": {
                    "$round": [
                        {
                            "$multiply": [
                                {"$divide": ["$count", {"$literal": 5600}]},
                                100,
                            ]
                        },
                        2,
                    ]
                },
            }
        },
    ]

    with get_mongo_client() as client:
        collection = client["sample_airbnb"]["listingsAndReviews"]
        return list(collection.aggregate(pipeline))

if __name__ == "__main__":
    results = run_unwind_aggregation()
    for doc in results:
        pprint.pprint(doc)
