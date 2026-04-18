from pymongo import MongoClient

client = MongoClient(
    "mongodb://admin:test@localhost:27017/?authSource=admin&readPreference=primary&ssl=false"
)
result = client["sample_airbnb"]["listingsAndReviews"].aggregate(
    [
        {"$match": {"address.country_code": "US"}},
        {"$sort": {"property_type": 1, "price": 1}},
        {
            "$group": {
                "_id": "$property_type",
                "count": {"$sum": 1},
                "average": {"$avg": "$price"},
                "cheaper": {
                    "$first": {
                        "name": "$name",
                        "price": "$price",
                        "address": "$address",
                    }
                },
                "expensive": {
                    "$last": {"name": "$name", "price": "$price", "address": "$address"}
                },
            }
        },
        {
            "$set": {
                "Property Type": "$_id",
                "Amount of properties": "$count",
                "Average Price": {"$round": ["$average", 2]},
                "Properties": [
                    {
                        "Type": "Cheaper",
                        "Name": "$cheaper.name",
                        "Price": "$cheaper.price",
                    },
                    {
                        "Type": "Expensive",
                        "Name": "$expensive.name",
                        "Price": "$expensive.price",
                    },
                ],
            }
        },
        {
            "$project": {
                "_id": 0,
                "count": 0,
                "average": 0,
                "cheaper": 0,
                "expensive": 0,
            }
        },
    ]
)
