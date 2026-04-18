from pymongo import MongoClient

client = MongoClient(
    "mongodb://admin:test@localhost:27017/?authSource=admin&readPreference=primary&ssl=false"
)
result = client["sample_airbnb"]["listingsAndReviews"].aggregate(
    [
        {"$addFields": {"address.country_code": "US"}},
        {"$sort": {"price": 1}},
        {"$limit": 5},
    ]
)
