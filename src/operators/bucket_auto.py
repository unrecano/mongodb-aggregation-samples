import pprint
from typing import Any, Dict, List

from src.db import get_mongo_client


def run_bucket_auto_aggregation() -> List[Dict[str, Any]]:
    """
    Executes an aggregation pipeline using $bucketAuto to automatically group documents 
    into a specified number of buckets based on their review scores rating.

    Returns:
        List[Dict[str, Any]]: A list of documents representing the automatically generated buckets.
    """
    pipeline = [
        {
            "$bucketAuto": {
                "groupBy": "$review_scores.review_scores_rating",
                "buckets": 4,
                "output": {
                    "count": {"$sum": 1}
                }
            }
        }
    ]

    with get_mongo_client() as client:
        collection = client["sample_airbnb"]["listingsAndReviews"]
        return list(collection.aggregate(pipeline))


if __name__ == "__main__":
    results = run_bucket_auto_aggregation()
    for result in results:
        pprint.pprint(result)
