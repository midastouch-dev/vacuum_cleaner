from flask import Flask, request, jsonify

app = Flask(__name__)

class VacuumCleaner:
	def __init__(self):
		self.current_room = 1

	def traverse_to(self, room):
		path = []
		room_passed_without_cleaning = 0;

		if room > self.current_room:
			path.extend(range(self.current_room + 1, room + 1))
			room_passed_without_cleaning += room - self.current_room - 1
		elif room < self.current_room:
			path.extend(range(self.current_room - 1, room - 1, -1))
			room_passed_without_cleaning += self.current_room - room - 1

		self.current_room = room

		return path, room_passed_without_cleaning

	def process_clearning_batches(self, cleaning_batches, priority_rooms):
		total_cleaned_rooms = 0
		total_batches = 0
		path_token = []
		room_passed_without_cleaning = 0

		for batch in cleaning_batches:
			total_batches += 1
			cleaned_in_batch = []

			for priority_room in priority_rooms:
				if priority_room in batch:
					path, rooms_without_cleaning = self.traverse_to(priority_room)
					path_token.extend(path)
					room_passed_without_cleaning += rooms_without_cleaning
					cleaned_in_batch.append(priority_room)
					total_cleaned_rooms += 1

			for room in batch:
				if room not in cleaned_in_batch:
					path, rooms_without_cleaning = self.traverse_to(room)
					path_token.extend(path)
					room_passed_without_cleaning += rooms_without_cleaning
					cleaned_in_batch.append(room)
					total_cleaned_rooms += 1

		return {
			"path_token": path_token,
			"total_cleaned_rooms": total_cleaned_rooms,
			"total_batches": total_batches,
			"rooms_passed_without_cleaning": room_passed_without_cleaning,
			"final_room": self.current_room,
		}

@app.route('/clean', methods=['POST'])
def clean():
	data = request.get_json()
	cleaning_batches = data.get("cleaning_batches")
	priority_rooms = data.get("priority_rooms")

	if cleaning_batches and priority_rooms:
		vacuum_cleaner = VacuumCleaner();
		result = vacuum_cleaner.process_clearning_batches(cleaning_batches, priority_rooms)
		return jsonify(result), 200
	else:
		return jsonify({"error": "Missing data"}), 400


@app.route('/')
def hello_vacuum_clear():
	return '<h1>Hello, Vacuum Cleaner!</h1>'

if __name__ == "__main__":
	app.run(host='0.0.0.0', debug=False, port=3000)
