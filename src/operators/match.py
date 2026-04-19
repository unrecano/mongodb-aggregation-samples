from typing import List, Dict, Any
from src.db import get_mongo_client
import pprint


def run_match_aggregation() -> List[Dict[str, Any]]:
    """
    Executes an aggregation pipeline using $match equivalent to adding a field and limiting results.

    Returns:
        List[Dict[str, Any]]: A list of aggregated documents matching the criteria.
    """
    pipeline = [
        {"$addFields": {"address.country_code": "US"}},
        {"$sort": {"price": 1}},
        {"$limit": 5},
    ]

    with get_mongo_client() as client:
        collection = client["sample_airbnb"]["listingsAndReviews"]
        return list(collection.aggregate(pipeline))


if __name__ == "__main__":
    results = run_match_aggregation()
    pprint.pprint(results)
