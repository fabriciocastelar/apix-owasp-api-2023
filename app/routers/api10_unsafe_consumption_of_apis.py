from fastapi import APIRouter, Request, HTTPException
import requests

router = APIRouter()

@router.get("/external/weather")
def get_weather(city: str = "London", api_key: str = "", request: Request = None):
    secure_mode = request.headers.get("X-Secure-Mode", "true").lower() == "true"

    if not api_key:
        raise HTTPException(status_code=400, detail="API Key is required for external weather API")

    external_api_url = f"https://api.weatherapi.com/v1/current.json?key={api_key}&q={city}" #https://app.swaggerhub.com/apis-docs/WeatherAPI.com/WeatherAPI/1.0.2

    try:
        response = requests.get(external_api_url, timeout=5, verify=False)  # Ignorando SSL para a demo
        external_data = response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch external API: {str(e)}")

    if secure_mode:
        if "location" not in external_data or "current" not in external_data:
            raise HTTPException(status_code=502, detail="Invalid data received from external API")

        return {
            "city": external_data["location"]["name"],
            "temp_celsius": external_data["current"]["temp_c"],
            "condition": external_data["current"]["condition"]["text"]
        }
    else:
        return external_data
