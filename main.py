from google import genai
import json
import os
import requests

# Load the environment variables from the .env file
from dotenv import load_dotenv

load_dotenv()

# =============================================================================
# Step 1: Define the Tool Schema (function declaration)
# =============================================================================
get_current_weather_declaration = {
    "type": "function",
    "name": "get_weather",
    "description": "Gets the current weather forecast for a city located in the U.S.",
    "parameters": {
        "type": "object",
        "properties": {
            "city": {
                "type": "string",
                "description": "A city name",
            }
        },
    },
}

 
# Native Python implementation of the tool
def get_current_weather(cityname: str):
    api_key: str | None = os.getenv("OPENWEATHER_API_KEY")
    base_url: str | None = os.getenv("OPENWEATHER_BASE_URL")

    if not api_key or not base_url:
        raise ValueError("Missing API key or Base URL in environment variables.")

    params: dict[str, str] = {
        "q": cityname,
        "appid": api_key,
        "units": "imperial",
    }

    response = requests.get(base_url, params=params)
    response.raise_for_status()

    print(response.json())
    return response.json()


# =============================================================================
# Step 2: Call LLM w/ function declarations:
# Send user prompt along with the function declaration(s) to the model.
# =============================================================================

client = genai.Client()
interaction = client.interactions.create(
    model="gemini-3.6-flash",
    input="What is the real-time weather in Leesburg?",
    tools=[get_current_weather_declaration],
)


fc_step = next(s for s in interaction.steps if s.type == "function_call")
print(fc_step)


# =============================================================================
# Step 3: Execute the function
# =============================================================================

if fc_step.name == "get_weather":
    city_arg = fc_step.arguments["city"]
    print(f"Executing local function for city: {city_arg}")
    api_result_json = get_current_weather(cityname=city_arg)

# =============================================================================
# Step 4: Send result back to model
# =============================================================================

final_interaction = client.interactions.create(
    model="gemini-3.6-flash",
    input=[
        {
            "type": "function_result",
            "name": fc_step.name,
            "call_id": fc_step.id,
            "result": [{"type": "text", "text": json.dumps(api_result_json)}],
        }
    ],
    tools=[get_current_weather_declaration],
    previous_interaction_id=interaction.id,
)

# Print the final human-readable answer from the LLM
print("\n--- Final Model Output ---")
print(final_interaction.output_text)
