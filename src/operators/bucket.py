import pprint
from typing import Any, Dict, List

from src.db import get_mongo_client


def run_bucket_aggregation() -> List[Dict[str, Any]]:
    """
    Executes an aggregation pipeline using $bucket to group documents into buckets
    based on their review scores rating.

    Returns:
        List[Dict[str, Any]]: A list of documents representing the buckets.
    """
    pipeline = [
        {
            "$bucket": {
                "groupBy": "$review_scores.review_scores_rating",
                "boundaries": [0, 50, 70, 85, 100],
                "default": "N/A",
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
    results = run_bucket_aggregation()
    for result in results:
        pprint.pprint(result)
