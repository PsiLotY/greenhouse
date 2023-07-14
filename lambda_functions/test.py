dictionary = {
    0: {'measure_name': 'temperature', 'temperature': 20, 'device_id': '002', 'timestamp': '2023-07-14 16:45:06.477000000'},
    1: {'measure_name': 'temperature', 'temperature': 20, 'device_id': '002', 'timestamp': '2023-07-14 16:45:01.492000000'},
    2: {'measure_name': 'temperature', 'temperature': 20.89, 'device_id': '002', 'timestamp': '2023-07-14 16:25:56.722000000'},
    3: {'measure_name': 'temperature', 'temperature': 20, 'device_id': '002', 'timestamp': '2023-07-14 16:25:51.679000000'},
    4: {'measure_name': 'temperature', 'temperature': 36.88, 'device_id': '007', 'timestamp': '2023-07-14 16:25:46.690000000'}
}

values_list = ['002', '007']
temperature_threshold = 25

def all_present_and_hot(temperature_data, device_ids):
    temperature_threshold = 25
    all_present = True
    for id in device_ids:
        # check if device id is present in temperature data
        if id not in [entry['device_id'] for entry in temperature_data.values()]:
            all_present = False
            break
        # check if at least one temperature value for device id is above threshold
        if not any(entry['temperature'] > temperature_threshold for entry in temperature_data.values() if entry['device_id'] == id):
            all_present = False
            break
    return all_present

print(all_present_and_hot(dictionary, values_list))