from pymongo import MongoClient

client = MongoClient(
    "mongodb://admin:test@localhost:27017/?authSource=admin&readPreference=primary&ssl=false"
)
result = client["sample_airbnb"]["listingsAndReviews"].aggregate(
    [
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
)
