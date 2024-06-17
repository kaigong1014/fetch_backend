from pydantic import BaseModel, Field
from typing import List
from fastapi import FastAPI, HTTPException
from uuid import uuid4
import math

class Item(BaseModel):
    shortDescription: str
    price: str

class Receipt(BaseModel):
    retailer: str
    purchaseDate: str
    purchaseTime: str
    items: List[Item]
    total: str

receipts = {}

def calculate_points(receipt: Receipt) -> int:
    points = 0

    #One point for every alphanumeric character in the retailer name
    points += sum(c.isalnum() for c in receipt.retailer)
    
    #50 points if the total is a round dollar amount with no cents
    if float(receipt.total) == int(float(receipt.total)):
        points += 50

    #25 points if the total is a multiple of 0.25
    if float(receipt.total) % 0.25 == 0:
        points += 25

    #5 points for every two items on the receipt
    points += (len(receipt.items) // 2) * 5

    #Points based on the length of item descriptions
    for item in receipt.items:
        if len(item.shortDescription.strip()) % 3 == 0:
            points += math.ceil(float(item.price) * 0.2)

    #6 points if the day in the purchase date is odd
    purchase_day = int(receipt.purchaseDate.split("-")[2])
    if purchase_day % 2 != 0:
        points += 6

    #10 points if the time of purchase is after 2:00pm and before 4:00pm
    hour, minute = map(int, receipt.purchaseTime.split(":"))
    if 14 <= hour < 16:
        points += 10

    return points

app = FastAPI()

@app.post("/receipts/process")
async def process_receipt(receipt: Receipt):
    receipt_id = str(uuid4())
    receipts[receipt_id] = receipt
    return {"id": receipt_id}

@app.get("/receipts/{id}/points")
async def get_points(id: str):
    if id not in receipts:
        raise HTTPException(status_code=404, detail="Receipt not found")
    receipt = receipts[id]
    points = calculate_points(receipt)
    return {"points": points}