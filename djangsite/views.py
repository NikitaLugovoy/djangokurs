import cv2
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from keras.models import load_model
from PIL import Image, ImageOps
import tensorflow as tf
import sqlite3
from datetime import datetime


# Assuming you have four classes, modify the classes list accordingly
classes = ["Airplanes", "Bikes", "Buses", "Cars", "Helicopters", "Ships", "Trains", "Trucks"]

filename = "djangsite/modeliskur (1).h5"
model = load_model(filename)

# Function to connect to the SQLite database
def connect_db():
    conn = sqlite3.connect('djangsite/fotosave.db')
    conn.row_factory = sqlite3.Row
    return conn

# Function to add photo info to the database
def add_photo_info(file_name, predicted_class, upload_time):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO photos (photo_link, class_name, upload_time) VALUES (?, ?, ?)",
            (file_name, predicted_class, upload_time)
        )
        conn.commit()
    except sqlite3.Error as e:
        print("Error adding photo info to the database:", str(e))
    finally:
        conn.close()

def home_page(request):
    if request.method == 'POST' and request.FILES:
        file = request.FILES['myfile1']
        files = Image.open(file)
        fs = FileSystemStorage()
        filename = fs.save(file.name, file)
        file_url = fs.url(filename)

        size = (180, 180)
        files = ImageOps.fit(files, size, Image.Resampling.LANCZOS)
        img_array = tf.keras.utils.img_to_array(files)
        img_array = tf.expand_dims(img_array, 0)

        predictions = model.predict_on_batch(img_array).flatten()
        predictions = tf.nn.sigmoid(predictions)

        # Assuming you are using a threshold of 0.5 for binary classification
        # If you have more than two classes, use argmax to get the class index
        predicted_class_index = tf.argmax(predictions, axis=-1)

        # Get the current time
        upload_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Save photo info to the database
        add_photo_info(file_url, classes[predicted_class_index.numpy()], upload_time)

        return render(request, 'home_page.html', {
            'file_url': file_url,
            'text': classes[predicted_class_index.numpy()]
        })

    return render(request, 'home_page.html')




def display_foto(request):
    conn = sqlite3.connect('djangsite/fotosave.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM photos")
    rows = cursor.fetchall()

    conn.close()

    return render(request, 'display_foto.html', {'photos': rows})

