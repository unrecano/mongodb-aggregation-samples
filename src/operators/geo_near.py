from typing import List, Dict, Any
from src.db import get_mongo_client
import pprint

def run_geo_near_aggregation() -> List[Dict[str, Any]]:
    """
    Executes an aggregation pipeline using $geoNear to find properties near a specific point.

    Returns:
        List[Dict[str, Any]]: A list of documents resulting from the aggregation pipeline.
    """
    pipeline = [
        {
            "$geoNear": {
                "near": {
                    "type": "Point",
                    "coordinates": [-73.95552676483872, 40.799483939486901],
                },
                "distanceField": "distance",
                "maxDistance": 30000,
                "spherical": True,
            }
        },
        {"$match": {"beds": {"$ne": 0}}},
        {"$project": {"distance": 1, "bedPrice": {"$divide": ["$price", "$beds"]}}},
        {
            "$group": {
                "_id": {
                    "$cond": {
                        "if": {"$lte": ["$distance", 2000]},
                        "then": "less than 2K",
                        "else": "greater than 2K",
                    }
                },
                "bedAverage": {"$avg": "$bedPrice"},
            }
        },
    ]

    with get_mongo_client() as client:
        collection = client["sample_airbnb"]["listingsAndReviews"]
        return list(collection.aggregate(pipeline))

if __name__ == "__main__":
    results = run_geo_near_aggregation()
    pprint.pprint(results)
