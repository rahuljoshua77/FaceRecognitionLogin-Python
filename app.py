import face_recognition, base64,os
cwd = os.getcwd()
from requests_html import HTMLSession
session = HTMLSession()
from io import BytesIO
import io
from multiprocessing import Pool

from flask import Flask, render_template, request, redirect, jsonify

# Inisialisasi aplikasi Flask
import numpy as np
application = Flask(__name__, static_url_path='/static')
from PIL import Image
from time import sleep
import urllib.request
from io import BytesIO
import io
import face_recognition, base64,os
cwd = os.getcwd()
from requests_html import HTMLSession
session = HTMLSession()

import face_recognition, base64,os
import pymysql

# Connect to the database

@application.route('/')
def index():
    return render_template('index.html')

@application.route('/login', methods=['POST'])
def login():
    basepath = os.path.abspath(".")
    # Create a cursor
    conn = pymysql.connect(
    host="HOST_DB",
    user="userNAME",
    password="Password",
    database="db_name"
    )
    cursor = conn.cursor()

    # Execute a SELECT statement
    cursor.execute("SELECT foto FROM tb_user")

    # Fetch all rows
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    # Create a list of image names
    image_names = [row[0] for row in rows]
    print(image_names)
    import urllib.request
    from PIL import Image

    image_files = []
    known_faces = {}

    for image_file in image_names:
        try:
            url = "https://WEB-FOR-IMAGE-SOURCE.comimages/profil/" + image_file
            save_path = os.path.join(basepath, 'mysite/static/images', image_file)
            urllib.request.urlretrieve(url, save_path)
            image = face_recognition.load_image_file(save_path)
            known_faces[image_file.split(".")[0]] = face_recognition.face_encodings(image)[0]
        except Exception as e:
            print(f"error {e}")
            pass
 
    conn = pymysql.connect(
    host="HOST_DB",
    user="userNAME",
    password="Password",
    database="db_name"
    )
    cursor = conn.cursor()

    # Execute a SELECT statement

    if request.method == 'POST':
        img_data = request.form.get("imgData")
        img_data = img_data.split(',')[1]
        img = face_recognition.load_image_file(BytesIO(base64.b64decode(img_data)))
        try:
            face_encodings = face_recognition.face_encodings(img)
            if len(face_encodings) == 0:
                return render_template('failed.html')
            face_encoding = face_encodings[0]
            print(face_encoding)
            face_distances = face_recognition.face_distance(list(known_faces.values()), face_encoding)
            best_match_index = np.argmin(face_distances)
            if face_distances[best_match_index] < 0.45:
                name = list(known_faces.keys())[best_match_index]
                cursor.execute(f"SELECT nama_lengkap FROM tb_user as tu where nik='{name}'")
                rows = cursor.fetchall()
                cursor.close()
                conn.close()
                return render_template('success.html', name=rows[0][0])
            else:
                return render_template('failed.html')
        except:
            return render_template('failed.html')



if __name__ == '__main__':
    application.run(debug=True)
