import pprint
from src.db import get_mongo_client
from typing import List, Dict, Any


def run_redact_aggregation() -> List[Dict[str, Any]]:
    """
    Executes an aggregation pipeline using $redact to filter documents based on a condition.

    Returns:
        List[Dict[str, Any]]: A list of documents from the aggregation.
    """
    pipeline = [
        {
            "$redact": {
                "$cond": {
                    "if": {"$gte": ["$review_scores.review_scores_rating", 95]},
                    "then": "$$KEEP",
                    "else": "$$PRUNE",
                }
            }
        },
        {"$count": "count"},
    ]

    with get_mongo_client() as client:
        collection = client["sample_airbnb"]["listingsAndReviews"]
        return list(collection.aggregate(pipeline))


if __name__ == "__main__":
    results = run_redact_aggregation()
    for doc in results:
        pprint.pprint(doc)
