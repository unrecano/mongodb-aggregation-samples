from typing import List, Dict, Any
from src.db import get_mongo_client
from bson import Code
import pprint


def run_accumulator_aggregation() -> List[Dict[str, Any]]:
    """
    Executes an aggregation pipeline using $accumulator to calculate custom statistics.

    Returns:
        List[Dict[str, Any]]: A list of documents from the aggregation.
    """
    pipeline = [
        {"$match": {"review_scores.review_scores_rating": {"$gt": 90}}},
        {"$addFields": {"amenitiesSize": {"$size": "$amenities"}}},
        {
            "$group": {
                "_id": None,
                "media": {
                    "$accumulator": {
                        "init": Code(
                            """
                            function () {
                                return { sum: 0, count: 0 };
                            }
                            """
                        ),
                        "accumulateArgs": ["$amenitiesSize"],
                        "accumulate": Code(
                            """
                            function (state, size) {
                                return {
                                    sum: state.sum + size,
                                    count: state.count + 1
                                };
                            }
                            """
                        ),
                        "merge": Code(
                            """
                            function (before, current) {
                                return {
                                    sum: before.sum + current.sum,
                                    count: before.count + current.count
                                };
                            }
                            """
                        ),
                        "finalize": Code(
                            """
                            function (state) {
                                return state.count > 0 ? (state.sum / state.count) : 0;
                            }
                            """
                        ),
                        "lang": "js",
                    }
                },
            }
        },
    ]

    with get_mongo_client() as client:
        db = client["sample_airbnb"]
        explanation = db.command(
            "explain",
            {"aggregate": "listingsAndReviews", "pipeline": pipeline, "cursor": {}},
            verbosity="executionStats",
        )
        return [explanation]


if __name__ == "__main__":
    results = run_accumulator_aggregation()
    pprint.pprint(results)
