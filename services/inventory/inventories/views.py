from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .mongo import inventory_collection
from .services import reserve_inventory, release_inventory, deduct_inventory


@api_view(["POST"])
def create_inventory(request):
    data = request.data

    doc = {
        "product_id": data["product_id"],
        "available_quantity": data["available_quantity"],
        "reserved_quantity": 0,
        "warehouse": data["warehouse"]
    }

    inventory_collection.insert_one(doc)

    return Response({"message": "Inventory created"}, status=201)


@api_view(["GET"])
def get_inventory(request, product_id):
    inv = inventory_collection.find_one(
        {"product_id": product_id},
        {"_id": 0}
    )

    if not inv:
        return Response({"error": "Not found"}, status=404)

    return Response(inv)


@api_view(["POST"])
def reserve(request):
    try:
        result = reserve_inventory(
            request.data["product_id"],
            request.data["quantity"]
        )
        return Response(result)
    except Exception as e:
        return Response({"error": str(e)}, status=400)


@api_view(["POST"])
def release(request):
    result = release_inventory(
        request.data["product_id"],
        request.data["quantity"]
    )
    return Response(result)


@api_view(["POST"])
def deduct(request):
    result = deduct_inventory(
        request.data["product_id"],
        request.data["quantity"]
    )
    return Response(result)