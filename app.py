from flask import Flask, request, jsonify

app = Flask(__name__)

"""
The VacuumCleaner class defines the function of vacuum cleaner. 
How to receive the comments, how to clean and which values are returned after working.
"""
class VacuumCleaner:
	"""
	Initializing the variable required here
	"""
	def __init__(self):
		self.current_room = 1 # The room number that the vacuum cleaner is located on for now
		self.cleaned_room = []; # The list of rooms the vacuum cleaner cleaned

	"""
	The vacuum move to cleaning room from current position and the current_room is set to the cleaning room.
	Return the rooms passed without cleaning and the path during movement.
	Assume doesn't clean again if the cleaning room is same as current room.
	"""
	def traverse_to(self, room):
		path = [] # The path the vacuum is moved to cleaning room from current room

		if room > self.current_room: # The vacuum move right
			path.extend(range(self.current_room + 1, room + 1))
			self.cleaned_room.append(room);
		elif room < self.current_room: # The vacuum move left
			path.extend(range(self.current_room - 1, room - 1, -1))
			self.cleaned_room.append(room);

		self.current_room = room

		return path

	"""
	The vacuum cleaner is received the cleaning command and return the result.
	It clean the rooms of priority rooms first and clean other rooms of batch.
	"""
	def process_clearning_batches(self, cleaning_batches, priority_rooms):
		total_cleaned_rooms = 0 # The tatal count of rooms cleaned by vacuum
		total_batches = 0 # The total count of batches processed
		traverse_path = [] # The path of vacuum cleaner traverse
		self.cleaned_room = []; # Initialized the cleaned rooms when start the cleaning

		# Get all batches(array) from cleaning batches(array of array)
		for batch in cleaning_batches:
			total_batches += 1 # Increase the total count of batches processed
			cleaned_in_batch = [] # The cleaned rooms in batch

			"""
			Clean the rooms in priority rooms first. 
			Assume that doesn't clean again if the batch has several numbers of same room.
			For example, the batch is [2,4,6,5,4], priority is [7,4]. In this case, the vacuum cleans the room 4 once.
			"""
			for priority_room in priority_rooms:
				if priority_room in batch:
					path = self.traverse_to(priority_room)
					traverse_path.extend(path)
					cleaned_in_batch.append(priority_room)
					total_cleaned_rooms += 1

			"""
			Clean the rooms that weren't included in priority. 
			Assume that cleans again if the same rooms located in the batch.
			For example, the batch is [6, 4, 2, 6], then the vacuum cleans the room 6 twice.
			But the vacuum cleans the room 6 once, if the batch is [6, 6, 4, 2].
			"""
			for room in batch:
				if room not in cleaned_in_batch:
					path = self.traverse_to(room)
					traverse_path.extend(path)
					total_cleaned_rooms += 1


		return {
			"cleaned_rooms": self.cleaned_room,
			"traverse_path": traverse_path,
			"total_cleaned_rooms": total_cleaned_rooms,
			"total_batches": total_batches,
			"rooms_passed_without_cleaning": len(traverse_path) - len(self.cleaned_room),
			"final_room": self.current_room,
		}

vacuum_cleaner = VacuumCleaner(); #Initialized the Vacuum Cleaner class.

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
