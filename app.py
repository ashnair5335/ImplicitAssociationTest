from flask import Flask, render_template, jsonify, request
import random
import os
import csv

app = Flask(__name__)

d = [
    'd1.png', 'd2.png', 'd3.png',
    'd4.png', 'd5.png', 'd6.png', 'd7.png'
]

s = [
    's1.png', 's2.png', 's3.png',
    's4.png', 's5.png', 's6.png', 's7.png'
]

p = [
    'p1.png','p2.png','p3.png',
    'p4.png','p5.png','p6.png','p7.png'
]

u = [
    'u1.png', 'u2.png', 'u3.png',
    'u4.png', 'u5.png', 'u6.png', 'u7.png'
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
@app.route('/get_images', methods=['GET'])
def get_images():
    round_number = int(request.args.get('round', 1))
    
    if round_number == 1:
        all_images = d + s
        print("Fetching images for Round 1 (Dolphins and Sharks)")
    elif round_number == 2:
        all_images = p + u
        print("Fetching images for Round 2 (Pleasant and Unpleasant Words)")
    elif round_number == 3:
        all_images = d + u + s + p
        print("Fetching images for Round 3 (All)")
    elif round_number == 4:
        all_images = d + u + s + p
        print("Fetching images for Round 4 (All)")
    elif round_number == 5:
        all_images = s + d
        print("Fetching images for Round 5 (Sharks and Dolphins)")
    elif round_number == 6:
        all_images = s + u + d + p
        print("Fetching images for Round 6 (All)")
    elif round_number == 7:
        all_images = s + u + d + p
        print("Fetching images for Round 7 (All)")
    else:
        all_images = []
        print("Invalid round number received.")
    
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
