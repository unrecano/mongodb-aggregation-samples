from pymongo import MongoClient

client = MongoClient(
    "mongodb://admin:test@localhost:27017/?authSource=admin&readPreference=primary&ssl=false"
)
result = client["sample_airbnb"]["listingsAndReviews"].aggregate(
    [
        {"$sort": {"address.market": 1, "price": -1}},
        {
            "$group": {
                "_id": "$address.market",
                "expensive": {"$first": {"name": "$name", "price": "$price"}},
            }
        },
        {"$out": "expensiveProperties"},
    ]
)
