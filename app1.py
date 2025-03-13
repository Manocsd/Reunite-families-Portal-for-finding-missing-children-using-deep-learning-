from flask import Flask,render_template,request,redirect,url_for,session,flash,Response
import sqlite3
import os
import base64
import cv2
import numpy as np
import dlib
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart  
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import smtplib
from email.utils import formataddr
import time
app=Flask(__name__)
app.secretkey="fgdfgdfgfgd"
database="new1.db"
def createtable():
    conn=sqlite3.connect(database)
    cursor=conn.cursor()
    cursor.execute("create table if not exists parents_details (id integer primary key autoincrement, name text, email text unique,phone text, password text)")
    cursor.execute("create table if not exists vol_details (id integer primary key autoincrement, name text, email text unique,phone text, password text)")
    cursor.execute("create table if not exists child_details(id integer primary key autoincrement, childname text, parentname text,phone text, email text, address text, aadhar text, imagefile1 blob,imagefile2 blob,imagefile3 blob,imagefile4 blob,imagefile5 blob)")
    cursor.execute("create table if not exists child_informa(id integer primary key autoincrement, childname text, volntname text,phone text, email text,address text, aadhar text, imagefile1 blob)")

    cursor.execute("create table if not exists accept_table (id integer primary key autoincrement, childname text, parentname text,phone text, email text, address text, aadhar text, imagefile1 blob,imagefile2 blob,imagefile3 blob,imagefile4 blob,imagefile5 blob)")
    cursor.execute('''create table if not exists table10 (id integer primary key autoincrement,child_id integer , childname text, parentname text,email text,phone text,  address text, aadhar text, location text,date DATE,missingchild blob
                                      )''')

    cursor.execute('''create table if not exists table100 (id integer primary key, childname text, volntname text,email text,phone text,  address text, aadhar text, location text,date DATE,missingchild blob
                                      )''')

    cursor.execute('''create table if not exists table9 (id integer primary key autoincrement ,child_id integer , childname text, parentname text,email text,phone text,  address text, aadhar text, location text,date DATE
                                     )''')

    cursor.execute('''create table if not exists table19 (id integer primary key  , childname text, volntname text,email text,phone text,  address text, aadhar text, location text,date DATE
                                     )''')
    conn.commit()
    conn.close()


createtable()   

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

import re

@app.route('/parents_details', methods=["GET", "POST"])
def parents_details():
    if request.method == "POST":
        # Extract form data
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        password = request.form['password']

        # Name validation: only letters and spaces
        if not re.match(r'^[A-Za-z\s]+$', name):
            return "Invalid name. Only letters and spaces are allowed."

        # Phone validation: must be 10 digits, starting with 9, 8, 7, or 6
        if not re.match(r'^[6-9]\d{9}$', phone):
            return "Invalid phone number. Must start with 9, 8, 7, or 6 and be 10 digits."

        # Email validation: correct email format
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            return "Invalid email format."

        # Connect to the database
        con = sqlite3.connect(database)
        cur = con.cursor()

        # Check if email or phone number already exists
        cur.execute("SELECT * FROM parents_details WHERE email = ? OR phone = ?", (email, phone))
        existing_user = cur.fetchone()

        if existing_user:
            message1="Email or phone number is already registered"
            return render_template('parents_details.html', message1=message1)

        # Insert the data if email and phone are not already registered
        cur.execute("INSERT INTO parents_details(name, phone, email, password) VALUES(?, ?, ?, ?)",
                    (name, phone, email, password))
        con.commit()
        con.close()

        return render_template('parent_login.html')

    return render_template('parents_details.html')
 
@app.route('/vol_details',methods=["GET","POST"])
def vol_details():
    if request.method=="POST":
         name=request.form['name']
         phone=request.form['phone']
         email=request.form['email']
         password=request.form['password']

         if not re.match(r'^[A-Za-z\s]+$', name):
            return "Invalid name. Only letters and spaces are allowed."

        # Phone validation: must be 10 digits, starting with 9, 8, 7, or 6
         if not re.match(r'^[6-9]\d{9}$', phone):
            return "Invalid phone number. Must start with 9, 8, 7, or 6 and be 10 digits."

        # Email validation: correct email format
         if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            return "Invalid email format."
         
         con=sqlite3.connect(database)
         cur=con.cursor()

         cur.execute("SELECT * FROM vol_details WHERE email = ? OR phone = ?", (email, phone))
         existing_user = cur.fetchone()

         if existing_user:
             message2="Email or phone number is already registered"
             return render_template('vol_details.html', message2=message2)

         
         cur.execute("insert into vol_details(name, phone, email, password)values(?,?,?,?)",(name, phone, email, password))
         con.commit()
         return render_template('vol_login.html')
    return render_template('vol_details.html')


@app.route('/parent_login',methods = ["GET","POST"])
def parent_login():
    if request.method=="POST":
        email=request.form['email']
        password=request.form['password']
        con=sqlite3.connect(database)
        cur=con.cursor()
        cur.execute("select * from parents_details where email=? and password=?",(email,password))
        data=cur.fetchone()
        if data is None:
            message='Incorrect Username or Password'
            return render_template('parent_login.html', message=message)        
        else:
             return render_template('child_details.html')
    return render_template('parent_login.html')

@app.route('/vol_login',methods = ["GET","POST"])
def vol_login():
    if request.method=="POST":
        email=request.form['email']
        password=request.form['password']
        con=sqlite3.connect(database)
        cur=con.cursor()
        cur.execute("select * from vol_details where email=? and password=?",(email,password))
        data=cur.fetchone()
        if data is None:
            message='Incorrect Username or Password'
            return render_template('vol_login.html', message=message)        
        else:
             return render_template('child_informa.html')
    return render_template('vol_login.html')


UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
    
import tempfile
import os

@app.route('/child_informa', methods=["GET", "POST"])
def child_informa():
    if request.method == "POST":
        
            childname = request.form['childname']
            volnname = request.form['volnname']
            phone = request.form['phone']
            email = request.form['email']
            address = request.form['address']
            aadhar = request.form['aadhar']
            imageefile1 = request.files['image1']

            # Read the image data
            blobdata1 = imageefile1.read()

            # Validate inputs
            if not re.match(r'^[A-Za-z\s]+$', childname):
                return "Invalid name. Only letters and spaces are allowed."

            if not re.match(r'^[A-Za-z\s]+$', volnname):
                return "Invalid name. Only letters and spaces are allowed."

            if not re.match(r'^[6-9]\d{9}$', phone):
                return "Invalid phone number. Must start with 9, 8, 7, or 6 and be 10 digits."

            if not re.match(r'^[1-9]\d{11}$', aadhar):
                return "Invalid Aadhar number. Must start with 1 to 12 digits."

            if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
                return "Invalid email format."

            con = sqlite3.connect(database)
            cur = con.cursor()
            cur.execute(
                "INSERT INTO child_informa(childname, volntname, phone, email, address, aadhar, imagefile1) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (childname, volnname, phone, email, address, aadhar, blobdata1)
            )
            print('d')
            con.commit()
            
            print('e')
            
            
            # Define folder path
            image_folder = os.path.join('images')
            os.makedirs(image_folder, exist_ok=True)  # Create folder if it doesn't exist

            # Save the image in the folder with a meaningful name
            image_path = os.path.join(image_folder, f'{childname}.jpg')
            with open(image_path, 'wb') as img_file:
                img_file.write(blobdata1)

            # Save the image temporarily using tempfile
            with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
                temp_file.write(blobdata1)
                temp_file_path = temp_file.name  # Temporary file path to pass to the function

            # Process and match the image using the temporary file path
            match_result = process_and_match_image(temp_file_path)
            print(match_result)


            
            return render_template('index.html', match_result=match_result)

  

    return render_template('child_informa.html')


b=[]
def process_and_match_image(image_path):
    print('process')
    training_data_folder = 'image_folder'  # Folder with pre-saved images
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
    face_recognizer = dlib.face_recognition_model_v1("dlib_face_recognition_resnet_model_v1.dat")

    # Load the uploaded image
    uploaded_image = cv2.imread(image_path)
    gray_uploaded = cv2.cvtColor(uploaded_image, cv2.COLOR_BGR2GRAY)
    faces_uploaded = detector(gray_uploaded)
    zero=0   
    if not faces_uploaded:
        zero=0
        return zero
    # Extract face encoding from the uploaded image
    for face in faces_uploaded:
        shape_uploaded = predictor(gray_uploaded, face)
        uploaded_face_encoding = face_recognizer.compute_face_descriptor(uploaded_image, shape_uploaded)

        # Compare with images in the training data folder
        for person_name in os.listdir(training_data_folder):
            person_folder = os.path.join(training_data_folder, person_name)
            if os.path.isdir(person_folder):
                for filename in os.listdir(person_folder):
                    if filename.endswith(('.jpg', '.jpeg', '.png')):
                        training_image_path = os.path.join(person_folder, filename)
                        training_image = cv2.imread(training_image_path)
                        gray_training = cv2.cvtColor(training_image, cv2.COLOR_BGR2GRAY)
                        faces_training = detector(gray_training)

                        for face in faces_training:
                            shape_training = predictor(gray_training, face)
                            training_face_encoding = face_recognizer.compute_face_descriptor(training_image, shape_training)

                            # Calculat distance between uploaded image and training image
                            distance = np.linalg.norm(np.array(uploaded_face_encoding) - np.array(training_face_encoding))

                            if distance < 0.5:  # Threshold for a match
                                
                                match_result = int(person_name)
                                con=sqlite3.connect(database)
                                cursor=con.cursor()
                                cursor.execute("SELECT id  FROM child_informa")
                                data=cursor.fetchall()
                                print(data)
                                label1=match_result
                                b.append(label1)
                                                       
                                cursor.execute("SELECT id,childname, volntname, phone, email, address, aadhar  FROM child_informa where id = ?",( label1,))
                                data1=cursor.fetchone()
                                print(data1)

                                location="Chennai"
                                currentdate =datetime.datetime.now()

                                data_to_insert = data1 + (location , currentdate,)
                                cursor.execute('INSERT  INTO table19 (id,childname, volntname,  phone, email,address, aadhar, location,date)  VALUES (?,?,?, ?, ?, ?, ?, ?, ?)',data_to_insert)
                                con.commit()
                                

                                
                                cursor.execute("SELECT id, childname, volntname,  phone, email,address, aadhar, location,date FROM table19 WHERE id = ? ORDER BY id DESC LIMIT 1", (b[-1],))
                                data1 = cursor.fetchone()
                                print(data1)
                                image_folder=f"images/{data1[1]}.jpg"
                                image_data = cv2.imread(image_folder)
                                image_bytes = cv2.imencode(f'{data1[1]}.jpg', image_data)[1].tobytes()

                                data_to_insert1 = data1 + (image_bytes,)
                                cursor.execute('INSERT  INTO table100 (id,childname, volntname, email, phone, address, aadhar, location,date,missingchild)  VALUES ( ?, ?, ?, ?, ?, ?,?,?,?,?)',data_to_insert1)
                                
                                con.commit()
                              
                                
                                
                                cursor.execute("SELECT * FROM accept_table WHERE id = ?", (match_result,))
                                result = cursor.fetchone()
                                print(result)
                                    
                                default_email = "lingesh.prowork@gmail.com"
                                
                                email=result[4]
                                print(email)
                                
                                sender_email = 'lingesh.prowork@gmail.com'
                                sender_password = 'fciktqtipmwjqjtd'
                                receiver_email =email
                                host = "smtp.gmail.com"
                                mmail = "lingesh.prowork@gmail.com"        
                                hmail = email
                                sender_name= "Volunteer"
                                receiver_name=data1[2]
                                msg = MIMEMultipart()
                                subject = "Found Your Child"
                                text =f"We Found One Missing  Child in {data1[7]} at {data1[8]}, \nChild Name:{data1[1]}, \nVolunteer Name:{data1[2]},\nVolunteer Address:{data1[5]},\nVolunteer Contact:{data1[3]},\nVolunteer Email:{data1[4]}"
                        ##             msg = MIMEText(text, 'plain')
                                msg.attach(MIMEText(text, 'plain'))
                                image_attachment = MIMEImage(image_bytes, name=f'{data1[1]}.jpg')
                                msg.attach(image_attachment)
                                msg['To'] = formataddr((receiver_name, hmail))
                                msg['From'] = formataddr((sender_name, mmail))
                                msg['Subject'] = 'Respected sir/mam  '
                                recipient_list = [hmail, default_email]
                                server = smtplib.SMTP(host, 587)
                                server.ehlo()
                                server.starttls()
                                    
                                server.login(mmail, sender_password)
                                server.sendmail(mmail, recipient_list, msg.as_string())
                                server.quit()
                                send="send"
                                print(send)
                                con.commit()
                                con.close()
                                return render_template('index.html', match_result=match_result)
                                

    return render_template('index.html', match_result=match_result)



@app.route('/child_details',methods=["GET","POST"])
def child_details():
    if request.method=="POST":
         childname=request.form['childname']
         parentname=request.form['parentname']
         phone=request.form['phone']
         email=request.form['email']
         address=request.form['address']
         aadhar=request.form['aadhar']
         imagefile1= request.files['image1']
         blobdata1= imagefile1.read()
         imagefile2= request.files['image2']
         blobdata2= imagefile2.read()
         imagefile3= request.files['image3']
         blobdata3= imagefile3.read()
         imagefile4= request.files['image4']
         blobdata4= imagefile4.read()
         imagefile5= request.files['image5']
         blobdata5= imagefile5.read()

         if not re.match(r'^[A-Za-z\s]+$', childname):
            return "Invalid name. Only letters and spaces are allowed."

         if not re.match(r'^[A-Za-z\s]+$', parentname):
            return "Invalid name. Only letters and spaces are allowed."

        # Phone validation: must be 10 digits, starting with 9, 8, 7, or 6
         if not re.match(r'^[6-9]\d{9}$', phone):
            return "Invalid phone number. Must start with 9, 8, 7, or 6 and be 10 digits."

         if not re.match(r'^[1-9]\d{11}$', aadhar):
            return "Invalid Aadhar number."

        # Email validation: correct email format
         if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            return "Invalid email format."

        
         con=sqlite3.connect(database)
         cur=con.cursor()
         cur.execute("insert into child_details(childname, parentname, email, phone, address, aadhar, imagefile1,imagefile2,imagefile3,imagefile4,imagefile5)values(?,?,?,?,?,?,?,?,?,?,?)",(childname, parentname, email, phone, address, aadhar, blobdata1,blobdata2,blobdata3,blobdata4,blobdata5))
         con.commit()

                
    

         
         return render_template('index.html')
    return render_template('child_details.html')



ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'admin'

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            return redirect('/details')
    return render_template('admin.html')



@app.route('/details',methods=['GET', 'POST'])
def details():
    if request.method == 'POST':
        print("details")
    return render_template('details.html')


@app.route('/view_pa', methods=["GET","POST"])
def view_pa():
    con=sqlite3.connect(database)
    cur=con.cursor()
    cur.execute("select * from child_details")
    results = cur.fetchall()
    con.commit()
    return render_template('view_pa.html', results=results)

@app.route('/view_vo', methods=["GET","POST"])
def view_vo():
    con=sqlite3.connect(database)
    cur=con.cursor()
    cur.execute("select * from child_informa")
    results = cur.fetchall()
    con.commit()
    return render_template('view_vo.html', results=results)

@app.template_filter('b64encode')
def base64_encode(data):
    return base64.b64encode(data).decode('utf-8')

##
##

@app.route('/accept_child', methods=["GET","POST"])
def accept_child():
    if request.method == "POST":
        try:
            child_id = request.form['number']
            print("Received child ID:", child_id)  # Add this line
            if not child_id:
                raise Exception("Child ID is missing")

            conn = sqlite3.connect(database)
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM child_details WHERE id = ?', (child_id,))
            child_data = cursor.fetchone()
            cursor.execute('INSERT INTO accept_table VALUES (?, ?, ?, ?, ?, ?, ?, ?,?,?,?,?)',child_data)
            if not child_data:
                raise Exception("Child data not found")
            cursor.execute("SELECT imagefile1,imagefile2,imagefile3,imagefile4  FROM child_details WHERE id = ?", (child_id,))
            image_file_names = cursor.fetchone()
            print(len(image_file_names))
            folder_path = os.path.join('image_folder', child_id)
            os.makedirs(folder_path, exist_ok=True)
            print(folder_path)
            for i, image_file_data in enumerate(image_file_names):
                if image_file_data:
                    image_path = os.path.join(folder_path, f'{child_id}_{i + 1}.jpg')
                    with open(image_path, 'wb') as image_file:
                        image_file.write(image_file_data)
                        print("success")
            cursor.execute('DELETE FROM child_details WHERE id = ?', (child_id,))
            conn.commit()
            conn.close()
                    
            return render_template('details.html')
        except Exception as e:           
           print("Error:", str(e))  
           return jsonify({"success": False, "error": str(e)})

    return render_template('admin.html')



@app.route('/accept_table', methods=["GET","POST"])
def accept_table():
    con=sqlite3.connect(database)
    cur=con.cursor()
    cur.execute("select * from accept_table")
    results = cur.fetchall()
    con.commit()
    return render_template('accept_table.html', results=results)

a=[]
criminals_notified = set()
criminals_last_notified = {}




detector = dlib.get_frontal_face_detector()
training_data_folder = 'image_folder'
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
face_recognizer = dlib.face_recognition_model_v1("dlib_face_recognition_resnet_model_v1.dat")
face_encodings = []
labels = []
for person_name in os.listdir(training_data_folder):
    person_folder = os.path.join(training_data_folder, person_name)
    if os.path.isdir(person_folder):
        person_id = int(person_name.replace('person', ''))  
        for filename in os.listdir(person_folder):
            if filename.endswith(('.jpg', '.jpeg', '.png')):
                image_path = os.path.join(person_folder, filename)
                image = cv2.imread(image_path)
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                faces = detector(gray)

                for face in faces:
                    shape = predictor(gray, face)
                    face_encoding = face_recognizer.compute_face_descriptor(image, shape)
                    face_encodings.append(face_encoding)
                    labels.append(person_id)
labels = np.array(labels)
face_encodings = np.array(face_encodings)

    
def generate_frames():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)
        print("finish")

        for face in faces:
            shape = predictor(gray, face)
            face_encoding = face_recognizer.compute_face_descriptor(frame, shape)
            distances = np.linalg.norm(face_encodings - face_encoding, axis=1)
            min_distance_idx = np.argmin(distances)
            min_distance = distances[min_distance_idx]
            print(min_distance)

            if min_distance < 0.5:
                label = labels[min_distance_idx]
                #print(label)
                imagefolder=f"new/{label}.jpg"
                image = cv2.imwrite(imagefolder, frame)
            else:
                label = "Unknown"

            x, y, w, h = face.left(), face.top(), face.width(), face.height()
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, f'Person {label}', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

            con=sqlite3.connect(database)
            cursor=con.cursor()
            cursor.execute("SELECT id  FROM accept_table")
            data=cursor.fetchall()
            print(data,label)

            if label in data:
                current_time = time.time()
                last_notified_time = criminals_last_notified.get(label, 0)

                if current_time - last_notified_time > 10:
                    criminals_last_notified[label] = current_time

                

                    label1=int(label)
                    a.append(label1)
               
                    cursor.execute("SELECT id,childname, parentname, email, phone, address, aadhar  FROM accept_table where id = ?",( label1,))
                    data1=cursor.fetchone()
             
                    location="chennai"
                    currentdate =datetime.datetime.now()
         
                    data_to_insert = data1 + (location , currentdate,)
                    cursor.execute('INSERT  INTO table9 (child_id, childname, parentname,  email, phone,address, aadhar, location,date)  VALUES (?,?, ?, ?, ?, ?, ?, ?,?)',data_to_insert)
                    con.commit()

                    cursor.execute("SELECT child_id, childname, parentname,  email, phone,address, aadhar, location,date FROM table9 WHERE child_id = ? ORDER BY id DESC LIMIT 1", (a[-1],))
                    data1 = cursor.fetchone()
                    print(data1)
                    image_folder=f"new/{data1[0]}.jpg"
                    image_data = cv2.imread(image_folder)
                    image_bytes = cv2.imencode(f'{data1[0]}.jpg', image_data)[1].tobytes()

                    data_to_insert1 = data1 + (image_bytes,)
                    cursor.execute('INSERT  INTO table10 (child_id, childname, parentname, email, phone, address, aadhar, location,date,missingchild)  VALUES (?, ?, ?, ?, ?, ?, ?,?,?,?)',data_to_insert1)


                    default_email = "pklingeshkumaar@gmail.com"  # Replace with your default email

                    email=data1[3]
                    
                    sender_email = 'lingesh.prowork@gmail.com'
                    sender_password = 'fciktqtipmwjqjtd'
                    receiver_email =email
                    host = "smtp.gmail.com"
                    mmail = "lingesh.prowork@gmail.com"        
                    hmail = email
                    sender_name= "admin"
                    receiver_name=data1[2]
                    msg = MIMEMultipart()
                    subject = "Found Your Child"
                    text =f"We Found One Missing  Child in {data1[7]} at {data1[8]}, \nChild Name:{data1[1]}, \nParent Name:{data1[2]},\nParent Address:{data1[5]},\nParent Contact{data1[4]}"
        ##             msg = MIMEText(text, 'plain')
                    msg.attach(MIMEText(text, 'plain'))
                    image_attachment = MIMEImage(image_bytes, name=f'{data1[0]}.jpg')
                    msg.attach(image_attachment)
                    msg['To'] = formataddr((receiver_name, hmail))
                    msg['From'] = formataddr((sender_name, mmail))
                    msg['Subject'] = 'Respected sir/mam'

                    recipient_list = [hmail, default_email]

                    server = smtplib.SMTP(host, 587)
                    server.ehlo()
                    server.starttls()
                    
                    server.login(mmail, sender_password)
                    server.sendmail(mmail, recipient_list, msg.as_string())

                    server.quit()
                    send="send"
                    print(send)
                    con.commit()
            cursor.close()
            con.close()

            
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        # Yield the frame to be displayed
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')   

    
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video', methods=['GET'])
def video():
    return render_template('track.html')

@app.route('/track', methods=['GET'])
def track():
    return render_template('track.html')

@app.route('/tracking', methods=['POST'])
def tracking():
    if request.method == 'POST':       
            generate_frames()
            return render_template('index.html')
    return render_template('track.html')

@app.route('/update', methods=['GET'])
def update():
    return render_template('update.html')



@app.route('/camera', methods=["GET","POST"])
def camera():
    con=sqlite3.connect(database)
    cursor=con.cursor()
    cursor.execute("SELECT * FROM table10")
    data = cursor.fetchall()
    return render_template('update.html', result=data)


@app.route('/volunter', methods=["GET","POST"])
def volunter():
    con=sqlite3.connect(database)
    cursor=con.cursor()
    cursor.execute("select * from table100")
    data1 = cursor.fetchall()
    print(data1)

    return render_template('update.html', result1=data1)


if __name__=="__main__":
    app.run(port=8000,debug=False)




