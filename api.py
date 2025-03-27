from flask import Flask, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
PORT = int(os.getenv("PORT", 5000))
EPL_API_URL = "https://api.football-data.org/v4/competitions/PL/standings"
API_KEY = os.getenv("API_KEY")  # Store your API key in a .env file

@app.route("/standings", methods=["GET"])
def get_standings():
    try:
        headers = {"X-Auth-Token": API_KEY}
        response = requests.get(EPL_API_URL, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        standings = [
            {
                "position": team["position"],
                "name": team["team"]["name"],
                "playedGames": team["playedGames"],
                "points": team["points"]
            }
            for team in data["standings"][0]["table"]
        ]
        
        return jsonify({"standings": standings})
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Failed to fetch standings", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(port=PORT, debug=True)

