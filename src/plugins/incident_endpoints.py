from datasette import hookimpl, Response
import json
import sqlite_utils
import hashlib
import requests
import dotenv
import os

dotenv.load_dotenv()
def get_hourly_weather(lat, lon, date):

    url = os.getenv("WEATHER_URL")

    body = {
        "lat": lat,
        "lon": lon,
        "start": date,
        "end": date
    }

    headers = {
        "x-rapidapi-key": os.getenv("WEATHER_API_KEY"),
        "x-rapidapi-host": os.getenv("WEATHER_API_HOST"),
    }

    response = requests.get(url, headers=headers, params=body)
    return response.json()




async def incident_unit_data(datasette, request):

    incident_id = request.url_vars["incident"]
    if not incident_id:
        return {"error": "No incident ID provided"}, 400
    
    db = sqlite_utils.Database("/mnt/data.db")

    incident_data = db["Incident"].get(incident_id)
    if not incident_data:
        return Response.json({
            "status": "error",
            "message": "Incident not found"
        }, status=404)
    
    incident_data = dict(incident_data)

    address_data = db["address"].get(incident_data["address_id"])

    weather = get_hourly_weather(address_data["latitude"], address_data["longitude"], incident_data["event_opened"].split("T")[0])
    incident_data["weather"] = weather["data"]
    department_data = db["Department"].get(incident_data["department_id"])
    incident_data["address"] = dict(address_data)
    incident_data["fire_department"] = dict(department_data)
    
    query = """
        SELECT 
            *
        FROM 
            Unit_Status us
        JOIN
            Apparatus a ON us.apparatus_id = a.id
        WHERE 
            a.incident_id = ?
        ORDER BY 
            us.timestamp
    """
    
    results = db.query(query, [incident_id])
    response = []
    for row in results:
        response.append(dict(row))

    return Response.json({
        "status": "ok",
        "responders": response,
        "incident": incident_data
    }, status=200)

async def create_incident(datasette, request):
    """
    Handle creation of a new incident.
    
    Args:
        datasette: The Datasette instance.
        request: The incoming request object.
    
    Returns:
        Response: JSON response with status
    """
    try:
        incident_data = await request.post_body()
        try: incident_data = json.loads(incident_data)
        except json.JSONDecodeError:
            return Response.json({
                "status": "error",
                "message": "Invalid JSON data"
            }, status=400)


        required_fields = ["address", "apparatus", "description", "fire_department"]
        missing_fields = [field for field in required_fields if field not in incident_data]
        if missing_fields:
            return Response.json({
                "status": "error",
                "message": f"Missing required fields: {', '.join(missing_fields)}"
            }, status=400)

        db = sqlite_utils.Database("/mnt/data.db")

        department = {k: v for k, v in incident_data["fire_department"].items() if k in db["Department"].columns_dict.keys()}
        department_id = db["Department"].insert(
            department
        ).last_pk

        address = {k: v for k, v in incident_data["address"].items() if k in db["address"].columns_dict.keys()}
        address_id = db["address"].insert(address).last_pk

        incident_data["description"]["address_id"] = address_id
        incident_data["description"]["department_id"] = department_id

        incident = {k: v for k, v in incident_data["description"].items() if k in db["Incident"].columns_dict.keys()}
        incident_id = db["Incident"].insert(incident).last_pk

        # make sure apparatus is an array
        if not isinstance(incident_data["apparatus"], list):
            incident_data["apparatus"] = [incident_data["apparatus"]]

        for apparatus in incident_data["apparatus"]:
            apparatus["incident_id"] = incident_id

            responder = {k: v for k, v in apparatus.items() if k in db["Apparatus"].columns_dict.keys()}
            apparatus_id = db["Apparatus"].insert(responder).last_pk
            for key in apparatus["unit_status"]:
                apparatus["unit_status"][key]["apparatus_id"] = apparatus_id
                apparatus["unit_status"][key]["status"] = key
                status = {k: v for k, v in apparatus["unit_status"][key].items() if k in db["Unit_Status"].columns_dict.keys()}
                db["Unit_Status"].insert(status)


        return Response.json({
            "status": "ok",
            "incident_id": incident_id
        }, status=201)

    except Exception as e:
        return Response.json({
            "status": "error",
            "message": str(e) 
        }, status=500)



@hookimpl
def register_routes():
    return [
        (r"^/-/create-incident$", create_incident),
        (r"^/-/incident-unit-data/(?P<incident>.*$)", incident_unit_data)
    ]
