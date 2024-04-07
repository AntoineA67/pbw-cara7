import json
import os

def read_data_from_car_json(folder_path):
		data = {}
		# List all files in the given directory
		for filename in os.listdir(folder_path):
			if filename.endswith('.json'):
				file_path = os.path.join(folder_path, filename)
				
				# Open and read the JSON file
				with open(file_path, 'r') as json_file:
					try:
						file_data = json.load(json_file)
						# Store the data using filename as key
						data[filename] = file_data
					except json.JSONDecodeError:
						print(f"Error reading {filename}. File is not valid JSON.")

		return data