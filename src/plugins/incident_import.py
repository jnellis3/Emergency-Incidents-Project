from datasette import hookimpl, Response
import json
import sqlite_utils
import hashlib


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


        required_fields = ["address", "aparatus", "description", "fire_department"]
        missing_fields = [field for field in required_fields if field not in incident_data]
        if missing_fields:
            return Response.json({
                "status": "error",
                "message": f"Missing required fields: {', '.join(missing_fields)}"
            }, status=400)

        db = sqlite_utils.Database("/mnt/data.db")
        department_id = db["Department"].upsert(
            incident_data["fire_department"], pk = "fd_id"
        ).last_pk

        address_id = db["address"].insert(
            incident_data["address"]
        ).last_pk

        incident_data["description"]["address_id"] = address_id
        incident_data["description"]["fd_id"] = department_id
        incident_id = db["Incident"].insert(incident_data["description"]).last_pk

        # make sure apparatus is an array
        if not isinstance(incident_data["apparatus"], list):
            incident_data["apparatus"] = [incident_data["apparatus"]]

        for apparatus in incident_data["apparatus"]:
            apparatus["incident_id"] = incident_id
            apparatus_id = db["Apparatus"].insert(apparatus)
            for key in apparatus["unit_status"]:
                apparatus["unit_status"][key]["apparatus_id"] = apparatus_id
                apparatus["unit_status"][key]["status"] = key
                db["Unit_Status"].insert(apparatus["unit_status"][key])

    except:
        pass



@hookimpl
def register_routes():
    return [
        (r"^/-/create-incident$", create_incident)
    ]
