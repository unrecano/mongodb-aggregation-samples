import pprint
from typing import Any, Dict, List

from bson import Code

from src.db import get_mongo_client


def run_function_aggregation() -> List[Dict[str, Any]]:
    """
    Executes an aggregation pipeline using $function to calculate custom values,
    such as the word count of a property description.

    Returns:
        List[Dict[str, Any]]: A list of documents from the aggregation.
    """
    pipeline = [
        {
            "$addFields": {
                "wordCount": {
                    "$function": {
                        "body": Code(
                            """
                            function (description) {
                                if (description) {
                                    var words = description.split(" ");
                                    return words.length;
                                } else {
                                    return 0;
                                }
                            }
                            """
                        ),
                        "args": ["$description"],
                        "lang": "js",
                    }
                }
            }
        },
        {
            "$group": {
                "_id": "$property_type",
                "averageWordCount": {
                    "$avg": "$wordCount"
                }
            }
        },
        {
            "$sort": {
                "averageWordCount": -1
            }
        }
    ]

    with get_mongo_client() as client:
        collection = client["sample_airbnb"]["listingsAndReviews"]
        return list(collection.aggregate(pipeline))


if __name__ == "__main__":
    results = run_function_aggregation()
    for result in results:
        pprint.pprint(result)
