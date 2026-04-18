from pymongo import MongoClient

client = MongoClient(
    "mongodb://admin:test@localhost:27017/?authSource=admin&readPreference=primary&ssl=false"
)
result = client["sample_analytics"]["customers"].aggregate(
    [
        {
            "$lookup": {
                "from": "accounts",
                "localField": "accounts",
                "foreignField": "account_id",
                "as": "account_info",
            }
        },
        {"$unwind": "$account_info"},
        {
            "$lookup": {
                "from": "transactions",
                "localField": "account_info.account_id",
                "foreignField": "account_id",
                "as": "account_transactions",
            }
        },
        {"$unwind": "$account_transactions"},
        {
            "$group": {
                "_id": "$name",
                "total": {"$sum": {"$size": "$account_transactions.transactions"}},
            }
        },
        {"$sort": {"total": -1}},
        {"$limit": 5},
        {"$project": {"_id": 0, "Name": "$_id", "total": 1}},
    ]
)
