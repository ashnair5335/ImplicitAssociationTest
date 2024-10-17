from flask import Flask, render_template, jsonify, request
import random
import os
import csv

app = Flask(__name__)

good_sharks = [
    'good_shark1.png', 'good_shark2.png', 'good_shark3.png',
    'good_shark4.png', 'good_shark5.png', 'good_shark6.png', 'good_shark7.png'
]

bad_sharks = [
    'bad_shark1.png', 'bad_shark2.png', 'bad_shark3.png',
    'bad_shark4.png', 'bad_shark5.png', 'bad_shark6.png', 'bad_shark7.png'
]

shown_images_list = []
selected_categories_list = []
response_times_list = []
all_data_list = []
csv_file_name = 'data.csv'


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/completion')
def completion():
    return render_template('completion.html')

@app.route('/get_images', methods=['GET'])
def get_images():
    all_images = good_sharks + bad_sharks
    random.shuffle(all_images)
    return jsonify(all_images)

test_results = []

def write_to_csv(data):
    file_exists = os.path.isfile(csv_file_name)
    
    with open(csv_file_name, mode='a', newline='') as csvfile:
        fieldnames = ['shown_image', 'selected_category', 'response_time']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        writer.writerow(data)

@app.route('/submit_data', methods=['POST'])
def submit_data():
    data = request.json

    shown_images_list.append(data['shown_image'])
    selected_categories_list.append(data['selected_category'])
    response_times_list.append(data['response_time'])
    all_data_list.append(data)

    data_file = open("data.txt", "a")
    data_file.write(str(data) + "\n")
    data_file.close()

    write_to_csv(data)

    print("Image:", data['shown_image'], "Category:", data['selected_category'], "Time:", data['response_time'], data)

    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
    print(shown_images_list)
    print(selected_categories_list)
    print(response_times_list)
