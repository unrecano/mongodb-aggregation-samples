from typing import List, Dict, Any
from src.db import get_mongo_client
import pprint

def run_out_aggregation() -> List[Dict[str, Any]]:
    """
    Executes an aggregation pipeline that saves the result into a new collection named 'expensiveProperties'.

    Returns:
        List[Dict[str, Any]]: A list of documents from the aggregation (empty since $out outputs to a collection).
    """
    pipeline = [
        {"$sort": {"address.market": 1, "price": -1}},
        {
            "$group": {
                "_id": "$address.market",
                "expensive": {"$first": {"name": "$name", "price": "$price"}},
            }
        },
        {"$out": "expensiveProperties"},
    ]

    with get_mongo_client() as client:
        collection = client["sample_airbnb"]["listingsAndReviews"]
        return list(collection.aggregate(pipeline))

if __name__ == "__main__":
    print("Ejecutando agregación y guardando en 'expensiveProperties'...")
    results = run_out_aggregation()
    print("Operación completada.")
