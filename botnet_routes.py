from fastapi import APIRouter, HTTPException
from typing import Dict
from botnet_service import get_botnet_service

router = APIRouter()

@router.post("/botnet")
async def botnet(request: Dict):
    """🤖 Single bot login using optimized botnet service"""
    botnet_service = get_botnet_service()
    username = request.get("username", "")
    password = request.get("password", "")
    appId = request.get("appId", "")
    result = await botnet_service.manage_bot_session(username, password, appId)
    if result.get("success"):
        return {
            "message": result["message"],
            "username": result["username"],
            "userId": result.get("userId", ""),
            "accessToken": result.get("accessToken", ""),
            "authCode": result.get("authCode", ""),
            "sync_result": result.get("sync_result", {}),
            "ws_result": result.get("ws_result", {}),
            "ws_response": result.get("ws_result", {}).get("response", ""),
        }
    else:
        return {"message": result.get("message", "Unknown error"), "success": False}

@router.post("/scrape-sjc")
async def scrape_sjc(request: Dict):
    """💳 Filter and validate credit cards from CSV data using Luhn algorithm & BIN lookup"""
    try:
        botnet_service = get_botnet_service()
        csv_data = request.get("csv_data", None)
        result = await botnet_service.scrape_sjc(csv_data=csv_data)
        if result.get("success"):
            return {
                "message": "Card filtering completed successfully",
                "status": "success",
                "data": result
            }
        else:
            return {
                "message": f"Card filtering failed: {result.get('error', 'Unknown error')}",
                "status": "error",
                "data": result
            }
    except Exception as e:
        return {
            "message": f"API error: {str(e)}",
            "status": "error"
        }

@router.post("/make-docs")
async def make_docs(request: Dict):
    """📄 Generate fake passport documents for testing purposes"""
    try:
        import random
        
        # Sample data for generating fake passports
        first_names = ["Oliver", "Harry", "Jack", "George", "Charlie", "Jacob", "Thomas", "Oscar", "William", "James",
                      "Emily", "Olivia", "Amelia", "Isla", "Ava", "Jessica", "Poppy", "Sophie", "Lily", "Grace"]
        last_names = ["Smith", "Taylor", "Brown", "Wilson", "Johnson", "Davies", "Robinson", "Wright", "Thompson", "Evans",
                     "Walker", "White", "Roberts", "Green", "Hall", "Wood", "Jackson", "Clarke", "Patel", "Khan"]
        streets = ["High Street", "Church Road", "Main Street", "Station Road", "Park Lane", "Victoria Road", "Green Lane",
                  "Manor Road", "Queens Road", "King Street", "The Avenue", "Mill Road", "School Lane", "North Road", "South Street"]
        cities = ["London", "Manchester", "Birmingham", "Leeds", "Liverpool", "Sheffield", "Bristol", "Newcastle", "Nottingham",
                 "Leicester", "Edinburgh", "Glasgow", "Cardiff", "Belfast", "Southampton"]
        postcodes = ["SW1A 1AA", "M1 1AB", "B1 1CD", "LS1 1EF", "L1 1GH", "S1 1IJ", "BS1 1KL", "NE1 1MN", "NG1 1OP",
                    "LE1 1QR", "EH1 1ST", "G1 1UV", "CF1 1WX", "BT1 1YZ", "SO14 0AA"]
        
        # Generate random number of passports (between 3 and 10)
        num_passports = random.randint(5, 5)
        passports = []
        
        for i in range(num_passports):
            # Generate random passport data
            passport_letter = random.choice(['G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'R', 'S'])
            passport_number = passport_letter + ''.join([str(random.randint(0, 9)) for _ in range(8)])
            
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            full_name = f"{first_name} {last_name}"
            
            # Generate random DOB (between 1960 and 2005)
            day = random.randint(1, 28)
            months = ["January", "February", "March", "April", "May", "June", "July", "August", 
                     "September", "October", "November", "December"]
            month = random.choice(months)
            year = random.randint(1960, 2005)
            dob = f"{day} {month} {year}"
            
            # Generate random address
            house_number = random.randint(1, 999)
            street = random.choice(streets)
            city = random.choice(cities)
            postcode = random.choice(postcodes)
            address = f"{house_number} {street}, {city} {postcode}"
            
            passports.append({
                "passport_number": passport_number,
                "name": full_name,
                "dob": dob,
                "address": address
            })
        
        return {
            "status": "success",
            "message": "Fake passport documents generated successfully",
            "data": {
                "passports": passports,
                "count": len(passports)
            }
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error generating documents: {str(e)}"
        }
