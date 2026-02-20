from datetime import datetime
from pymongo import ReturnDocument
from .mongo import inventory_collection


def reserve_inventory(product_id, quantity):
    result = inventory_collection.find_one_and_update(
        {
            "product_id": product_id,
            "available_quantity": {"$gte": quantity}
        },
        {
            "$inc": {
                "available_quantity": -quantity,
                "reserved_quantity": quantity
            },
            "$set": {"updated_at": datetime.utcnow()}
        },
        return_document=ReturnDocument.AFTER
    )

    if not result:
        raise Exception("Insufficient stock")

    result.pop("_id", None)
    return result


def release_inventory(product_id, quantity):
    result = inventory_collection.find_one_and_update(
        {"product_id": product_id},
        {
            "$inc": {
                "available_quantity": quantity,
                "reserved_quantity": -quantity
            }
        },
        return_document=ReturnDocument.AFTER
    )

    result.pop("_id", None)
    return result


def deduct_inventory(product_id, quantity):
    result = inventory_collection.find_one_and_update(
        {"product_id": product_id},
        {
            "$inc": {"reserved_quantity": -quantity}
        },
        return_document=ReturnDocument.AFTER
    )

    result.pop("_id", None)
    return result