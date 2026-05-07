# 🌤️ Weather App

A Flask web application that lets users search for any city and view the current weather with icons, detailed stats, and a 5-day forecast.

## Features

- 🔍 **City Search** — Enter any city name to instantly fetch live weather data
- 🌡️ **Current Conditions** — Temperature, feels-like, humidity, wind speed, and UV index
- 🌤️ **Weather Icons** — Emoji icons mapped to WMO weather codes (clear, cloudy, rain, snow, etc.)
- 📅 **5-Day Forecast** — Daily high/low temperatures and weather icons for the next 5 days
- 🌡️ **°F / °C Toggle** — Switch between Fahrenheit and Celsius with a single click
- ⚠️ **Error Handling** — Friendly messages for invalid city names or API issues
- 📱 **Responsive Design** — Works on desktop and mobile

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python / Flask |
| Weather API | [Open-Meteo](https://open-meteo.com/) (free, no API key needed) |
| Templating | Jinja2 |
| Frontend | HTML, CSS (no frameworks) |

## Project Structure

```
weather-app/
├── calculator.py          # Flask app — routes and API logic
├── templates/
│   └── weather.html       # Single-page Jinja2 template with inline CSS
├── README.md
└── sample.js
```

## Getting Started

### Prerequisites

- Python 3.8+
- pip

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/gilmarrrrr/weather-app.git
   cd weather-app
   ```

2. Install dependencies:
   ```bash
   pip install flask requests
   ```

3. Run the app:
   ```bash
   python calculator.py
   ```

4. Open your browser and go to: `http://localhost:5000`

## Usage

1. Type a city name in the search box (e.g. `London`, `Tokyo`, `New York`)
2. Click **Search**
3. View current weather and the 5-day forecast
4. Toggle between **°F** and **°C** using the buttons above the weather card

## API

This app uses two endpoints from [Open-Meteo](https://open-meteo.com/):

- **Geocoding** — `https://geocoding-api.open-meteo.com/v1/search` — converts city name to coordinates
- **Forecast** — `https://api.open-meteo.com/v1/forecast` — fetches current weather and daily forecast

No API key is required.

## Roadmap

- [x] Current weather with icons
- [x] 5-day forecast
- [x] °F / °C toggle
- [ ] [Recent search history](https://github.com/gilmarrrrr/weather-app/issues/3)

## License

MIT
