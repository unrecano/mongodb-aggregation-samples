from pymongo import MongoClient

client = MongoClient(
    "mongodb://admin:test@localhost:27017/?authSource=admin&readPreference=primary&ssl=false"
)
result = client["sample_airbnb"]["listingsAndReviews"].aggregate(
    [
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
)
