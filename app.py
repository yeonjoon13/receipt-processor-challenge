from flask import Flask, request, jsonify, abort
from decimal import Decimal
import uuid
import math
from datetime import datetime, time

app = Flask(__name__)

# In-memory storage for receipts
temp_database = {}

# Function to calculate points
def calculatePoints(receipt):
    totalPoints = 0

    # Rule 1: Alphanumeric characters in retailer name
    retailer = receipt.get("retailer", "")
    count = 0
    for character in retailer:
        if character.isalnum(): count += 1
    totalPoints += count

    total = Decimal(receipt.get("total", "0"))

    # Rule 2: Round dollar total
    totalPoints += 50 if float(total) - int(float(total)) == 0.0 else 0

    # Rule 3: Total is a multiple of 0.25
    totalPoints += 25 if int(100*float(total))%25 == 0 else 0

    # Rule 4: Every two items
    items = receipt.get("items", [])
    totalPoints += (len(items) // 2) * 5

    # Rule 5: Item descriptions multiple of 3 
    for item in items:
        description = item.get("shortDescription", "").strip()
        if description and len(description) % 3 == 0:
            price = float(item.get("price")) * 0.2
            totalPoints += math.ceil(price)

    # Rule 6: Odd purchase day
    purchase_date = receipt.get("purchaseDate", "")
    if purchase_date:
        dt = datetime.strptime(purchase_date, "%Y-%m-%d")
        if dt.day % 2 != 0: totalPoints += 6

    # Rule 7: Purchase time between 12:00 and 14:00
    purchase_time = receipt.get("purchaseTime", "")
    if purchase_time:
        t = datetime.strptime(purchase_time, "%H:%M").time()
        lower = datetime.strptime("14:00", "%H:%M").time()
        upper = datetime.strptime("16:00", "%H:%M").time()
        if lower < t < upper: totalPoints += 10

    return totalPoints

@app.route("/receipts/process", methods=["POST"])
def process_receipt():
    receipt = request.get_json()
    generated_id = str(uuid.uuid4())
    temp_database[generated_id] = calculatePoints(receipt)

    return jsonify({"id": generated_id})

@app.route("/receipts/<receipt_id>/points", methods=["GET"])
def get_points(receipt_id):
    if receipt_id not in temp_database:
        abort(404, "Receipt not found")
    return jsonify({"points": temp_database[receipt_id]})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
