from flask import Flask, render_template, jsonify, request
import requests

app = Flask(__name__)

USWTDB_API_BASE_URL = "https://energy.usgs.gov/api/uswtdb/v1"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/states')
def get_states():
    try:
        response = requests.get(f"{USWTDB_API_BASE_URL}/turbines?select=t_state&order=t_state.asc")
        response.raise_for_status()
        data = response.json()
        states = sorted(list(set([turbine['t_state'] for turbine in data if turbine['t_state']])))
        return jsonify(states)
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/turbines')
def get_turbines():
    state = request.args.get('state')
    if not state:
        return jsonify({"error": "State parameter is required"}), 400

    try:
        # Fetch turbines for the selected state, selecting relevant fields
        response = requests.get(f"{USWTDB_API_BASE_URL}/turbines?t_state=eq.{state}&select=p_name,t_state,t_model,t_cap,t_rd,t_hh,p_year&order=p_name.asc")
        response.raise_for_status()
        turbines = response.json()
        return jsonify(turbines)
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
