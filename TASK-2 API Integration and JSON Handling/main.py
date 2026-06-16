import requests

# Your API key from OpenWeatherMap
API_KEY = "96fe4e5b45bf87c217596e65e1f5075d"

# Base URL of the API
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def get_weather(city):
    """
    Fetch weather data from API
    """

    # Parameters sent to API
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    try:
        # Sending GET request to API
        response = requests.get(BASE_URL, params=params)

        # Convert JSON response into dictionary
        data = response.json()

        # Handle API errors
        if response.status_code != 200:
            print("API Error:", data.get("message"))
            return None

        return data

    except requests.exceptions.ConnectionError:
        print("Connection Error! Check internet.")

    except requests.exceptions.Timeout:
        print("Request Timed Out!")

    except requests.exceptions.RequestException as e:
        print("Something went wrong:", e)

    return None


def display_weather(data):
    """
    Display important weather information
    """

    # Extracting data from JSON response
    city = data["name"]
    country = data["sys"]["country"]
    temperature = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    weather = data["weather"][0]["description"]
    wind_speed = data["wind"]["speed"]

    print("\n====== WEATHER REPORT ======")
    print(f"City: {city}, {country}")
    print(f"Temperature: {temperature}°C")
    print(f"Humidity: {humidity}%")
    print(f"Weather: {weather}")
    print(f"Wind Speed: {wind_speed} m/s")
    print("============================")


def main():

    print("\n🌦 WEATHER INFORMATION FINDER 🌦")

    # User input
    city = input("Enter city name: ")

    # Fetch weather data
    weather_data = get_weather(city)

    # Check if data exists
    if weather_data:
        display_weather(weather_data)

    else:
        print("Could not fetch weather data.")


# Run program
if __name__ == "__main__":
    main()