from flask import Flask, request, jsonify
from vacuumcleaner.vacuumcleaner import VacuumCleaner

app = Flask(__name__)

vacuum_cleaner = VacuumCleaner() #Initialized the Vacuum Cleaner class.

"""
Received the comments via API with 2 parameters, cleaning_batches and priority_rooms.
The cleaning_batches is the array of array to clean the rooms.
The priority_rooms is the array of rooms to clean first. 
"""
@app.route('/clean', methods=['POST'])
def clean():
	data = request.get_json()
	cleaning_batches = data.get("cleaning_batches") # The array of array rooms that cleans
	priority_rooms = data.get("priority_rooms") # The array rooms that cleans first

	if cleaning_batches and priority_rooms: # Check that the all parameters are correct.
		result = vacuum_cleaner.process_clearning_batches(cleaning_batches, priority_rooms)
		return jsonify(result), 200
	else: # If the parameters are incorrect, return the missing data message.
		return jsonify({"error": "Missing data"}), 400

"""
Default route of project
"""
@app.route('/')
def hello_vacuum_clear():
	return '<h1>Hello, Vacuum Cleaner!</h1>'

"""
Run the project as the IP is 0.0.0.0, the port is 3000.
"""
if __name__ == "__main__":
	app.run(host='0.0.0.0', debug=False, port=3000)
