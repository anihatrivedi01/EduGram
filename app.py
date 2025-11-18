from flask import Flask, render_template, request, redirect, url_for, session, flash
import pyrebase
from datetime import datetime
from textblob import TextBlob

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Change this to something unique!

#Firebase Configuration
firebaseConfig = {
  "apiKey": "AIzaSyAaZ5em9oIxL8EEmGi_PDzxHy-PbmtGhcM",
  "authDomain": "edu-platform-91bbd.firebaseapp.com",
  "projectId": "edu-platform-91bbd",
 "storageBucket" : "edu-platform-91bbd.firebasestorage.app",
  'databaseURL': 'https://edu-platform-91bbd-default-rtdb.asia-southeast1.firebasedatabase.app/',
  "messagingSenderId": "1086137258887",
  "appId": "1:1086137258887:web:520fd34667d2a31f6e3922",
  "measurementId": "G-5F5YCKP9VG"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()

#Home Page
@app.route('/')
def home():
    courses = db.child("courses").get().val()
    if not courses:
        courses = {}

    current_user = None
    enrolled = {}

    # If a user is logged in, fetch their user data (including enrolled courses)
    if 'user' in session:
        try:
            uid = session['user'].get('localId')
            if uid:
                user_data = db.child("users").child(uid).get().val()
                # Normalize to dict and extract enrolled map safely
                if isinstance(user_data, dict):
                    current_user = user_data
                    enrolled = user_data.get('enrolled') or {}
                    # Ensure enrolled is a dict (sometimes firebase returns list/OrderedDict)
                    if not isinstance(enrolled, dict):
                        enrolled = dict(enrolled) if enrolled else {}
        except Exception as e:
            print("Error fetching user data for home:", e)
            current_user = None
            enrolled = {}

    return render_template('index.html', courses=courses, current_user=current_user, enrolled=enrolled)

#Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        phone = request.form.get('phone', '')
        age = request.form.get('age', '')
        gender = request.form.get('gender', '')
        address = request.form.get('address', '')
        role = request.form.get('role', 'student')
        profile_pic = request.files.get('profile_pic')

        try:
            # Create user
            user = auth.create_user_with_email_and_password(email, password)
            uid = user['localId']

            # Upload profile picture if provided
            import requests

# Upload profile picture manually to Firebase Storage
            profile_url = None
            if profile_pic:
               try:
        # Get the user's ID token for authentication
                 id_token = user['idToken']

                 storage_bucket = "edu-platform-91bbd.firebasestorage.app"

                 file_name = f"profile_pics/{uid}.jpg"

                 upload_url = f"https://firebasestorage.googleapis.com/upload/storage/v1/b/{storage_bucket}/o?uploadType=media&name={file_name}"

                 headers = {"Authorization": f"Bearer {id_token}"}

                 upload_response = requests.post(upload_url, headers=headers, data=profile_pic.read())
                 upload_response.raise_for_status()

        # Once uploaded, construct the download URL
                 profile_url = f"https://firebasestorage.googleapis.com/v0/b/{storage_bucket}/o/{file_name.replace('/', '%2F')}?alt=media"

               except Exception as upload_error:
                 print("Profile picture upload failed:", upload_error)
                 flash("Profile picture upload failed, but registration continued.", "warning")



            # Save to Realtime DB
            data = {
                'name': name,
                'email': email,
                'phone': phone,
                'age': age,
                'gender': gender,
                'address': address,
                'role': role,
                'profile_pic': profile_url or "",
                'enrolled': {}
            }
            db.child('users').child(uid).set(data)

            flash('Account created successfully! Please log in.', 'success')
            return redirect(url_for('login'))

        except Exception as e:
            err = str(e)
            if "EMAIL_EXISTS" in err:
                flash("This email is already registered. Please log in instead.", "warning")
            else:
                flash(f"Registration failed: {err}", "danger")
            return redirect(url_for('register'))

    return render_template('register.html')

#Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            user = auth.sign_in_with_email_and_password(email, password)
            session['user'] = user
            uid = user['localId']

            user_data = db.child("users").child(uid).get().val()
            session['role'] = user_data.get('role')  # 👈 store role in session

            flash("Logged in successfully!")

            # Redirect based on role
            if session['role'] == 'faculty':
                return redirect(url_for('faculty_dashboard'))
            else:
                return redirect(url_for('profile'))

        except Exception as e:
            flash("Invalid credentials. Please try again.")
            print("Login Error:", e)

    return render_template('login.html')



#Logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    flash("Logged out successfully.")
    return redirect(url_for('home'))

#Profile Page
@app.route('/profile')
def profile():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    user = session['user']
    uid = user['localId']

    # Fetch user info
    user_data = db.child("users").child(uid).get().val() or {}

    # Fetch enrolled courses (for students)
    enrolled = user_data.get('enrolled', {}) or {}

    # Fetch all courses
    courses = db.child("courses").get().val() or {}

    # If faculty, try to pull additional info from 'faculties'
    if user_data.get("role") == "faculty":
        faculties = db.child("faculties").get().val() or {}
        for fid, f in faculties.items():
            if f.get("email") == user_data.get("email") or f.get("name") == user_data.get("name"):
                # Merge faculty-specific fields into user_data
                user_data["subject"] = f.get("subject")
                user_data["bio"] = f.get("bio")
                user_data["contact"] = f.get("contact")
                break

    return render_template(
        'profile.html',
        user=user_data,
        enrolled=enrolled,
        courses=courses
    )



# Edit Profile
@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if 'user' not in session:
        flash("Please log in to edit your profile.", "warning")
        return redirect(url_for('login'))

    uid = session['user']['localId']
    user_data = db.child("users").child(uid).get().val() or {}

    if request.method == 'POST':
        try:
            # Collect form inputs
            name = request.form.get('name')
            phone = request.form.get('phone', '')
            age = request.form.get('age', '')
            gender = request.form.get('gender', '')
            address = request.form.get('address', '')
            profile_pic = request.files.get('profile_pic')

            # Prepare update data
            updated_data = {
                'name': name,
                'phone': phone,
                'age': age,
                'gender': gender,
                'address': address
            }

            # Handle profile picture upload
            if profile_pic and profile_pic.filename:
                try:
                    storage = firebase.storage()
                    storage_path = f"profile_pics/{uid}.jpg"
                    storage.child(storage_path).put(profile_pic)
                    profile_url = storage.child(storage_path).get_url(None)
                    updated_data['profile_pic'] = profile_url
                except Exception as e:
                    print("Profile picture upload failed:", e)
                    flash("Profile picture upload failed. Changes saved without it.", "warning")

            # Update Realtime Database
            db.child("users").child(uid).update(updated_data)
            

            flash("Profile updated successfully!", "success")
            return redirect(url_for('profile'))

        except Exception as e:
            print("Error updating profile:", e)
            flash("An error occurred while updating your profile.", "danger")

    return render_template('edit_profile.html', user=user_data)

# edit faculty Profile
@app.route('/edit_faculty/<faculty_id>', methods=['GET', 'POST'])
def edit_faculty(faculty_id):
    faculty = db.child("faculties").child(faculty_id).get().val() or {}

    if request.method == 'POST':
        updated_data = {
            "name": request.form.get("name"),
            "email": request.form.get("email"),
            "contact": request.form.get("contact"),
            "subject": request.form.get("subject"),
            "bio": request.form.get("bio")
        }
        db.child("faculties").child(faculty_id).update(updated_data)
        flash("Faculty info updated successfully!", "success")
        return redirect(url_for('admin_dashboard'))  # or wherever you list faculties

    return render_template('edit_faculty.html', faculty=faculty)

#Faculty Page
@app.route('/faculty')
def faculty():
    faculties = db.child("faculties").get().val()
    if faculties is None:
        faculties = {}
    return render_template("faculty.html", faculties=faculties)

@app.route('/enroll/<course_id>')
def enroll(course_id):
    if 'user' not in session:
        flash("Please log in to enroll.")
        return redirect(url_for('login'))

    uid = session['user']['localId']
    try:
        # Use set or update to ensure it's stored as { course_id: True }
        db.child("users").child(uid).child("enrolled").update({course_id: True})
        flash("You’ve successfully enrolled in the course!")
    except Exception as e:
        print("Enroll error:", e)
        flash("Could not enroll. Try again later.")
    return redirect(url_for('profile'))


# # quiz route
# @app.route('/quiz/<course_id>')
# def quiz(course_id):
#     quiz_data = db.child("quizzes").child(course_id).get().val()
#     if quiz_data is None:
#         quiz_data = {}
#     return render_template("quiz.html", quiz=quiz_data, course_id=course_id)

#Course Details
@app.route("/course/<course_id>")
def course_detail(course_id):
    course = db.child("courses").child(course_id).get().val()
    enrolled = False

    if 'user' in session:
        uid = session['user']['localId']
        user_data = db.child("users").child(uid).get().val()
        enrolled_courses = user_data.get("enrolled", {})
        enrolled = enrolled_courses.get(course_id, False)

    return render_template("course_detail.html", course=course, course_id=course_id, enrolled=enrolled)



# faculty dashboard route
@app.route('/faculty_dashboard')
def faculty_dashboard():
    if 'user' not in session:
        flash("Please log in first.")
        return redirect(url_for('login'))

    if session.get('role') != 'faculty':
        flash("Access denied! Faculty only.")
        return redirect(url_for('home'))

    user = session['user']
    user_data = db.child("users").child(user['localId']).get().val()
    return render_template("faculty_dashboard.html", user=user_data)


# add courses
@app.route("/add_course", methods=["GET", "POST"])
def add_course():
    if request.method == "POST":
        title = request.form["title"]
        text = request.form["text"]
        
        # Collect units dynamically
        units = {}
        for key in request.form:
            if key.startswith("unit_title_"):
                index = key.split("_")[-1]
                unit_title = request.form[key]
                unit_pdf = request.form.get(f"unit_pdf_{index}", "")
                unit_video = request.form.get(f"unit_video_{index}", "")
                units[f"unit{index}"] = {
                    "title": unit_title,
                    "pdf": unit_pdf,
                    "video": unit_video
                }

        course_data = {
            "title": title,
            "text": text,
            "units": units
        }

        db.child("courses").push(course_data)
        flash("Course added successfully!", "success")
        return redirect(url_for("faculty_dashboard"))

    return render_template("add_course.html")


@app.route('/add_faculty', methods=['POST'])
def add_faculty():
    if 'user' not in session or session.get('role') != 'faculty':
        flash("Access denied!")
        return redirect(url_for('home'))

    name = request.form['name']
    subject = request.form['subject']
    bio = request.form['bio']

    try:
        db.child("faculties").push({
            "name": name,
            "subject": subject,
            "bio": bio,
            "contact": request.form.get('contact'),
            "email": request.form.get('email')
        })
        flash("Faculty added successfully!")
    except Exception as e:
        print("Error adding faculty:", e)
        flash("Failed to add faculty.")

    return redirect(url_for('faculty_dashboard'))

@app.route('/doubts', methods=['GET', 'POST'])
def doubts():
    user = session.get('user')
    if not user:
        flash("Please log in to view or post doubts.", "warning")
        return redirect(url_for('login'))

    user_id = user['localId']
    user_email = user.get('email', 'Anonymous')

    if request.method == 'POST':
        # Check if user is posting a question or an answer
        if 'question' in request.form:
            # Posting a new doubt
            question = request.form['question']

            doubt_data = {
                "user_id": user_id,
                "user_email": user_email,
                "question": question,
                "answers": {}
            }

            db.child("doubts").push(doubt_data)
            flash("Your doubt has been posted!", "success")
        
        elif 'answer' in request.form:
            # Posting an answer to a specific doubt
            doubt_id = request.form['doubt_id']
            answer_text = request.form['answer']

            answer_data = {
                "answer_text": answer_text,
                "answered_by": user_email
            }

            db.child("doubts").child(doubt_id).child("answers").push(answer_data)
            flash("Your answer has been added!", "success")

        return redirect(url_for('doubts'))

    # Fetch all doubts
    all_doubts = db.child("doubts").get().val() or {}

    # Separate user’s doubts
    my_doubts = {k: v for k, v in all_doubts.items() if v.get("user_id") == user_id}

    return render_template("doubts.html", all_doubts=all_doubts, my_doubts=my_doubts)



@app.route('/doubts/<doubt_id>/answer', methods=['POST'])
def add_answer(doubt_id):
    user = session.get('user', 'Faculty')
    answer_text = request.form['answer']

    answer_data = {
        "user": user,
        "text": answer_text
    }

    db.child("doubts").child(doubt_id).child("answers").push(answer_data)
    flash("Your answer has been added!", "success")
    return redirect(url_for('doubts'))

# assignments
@app.route("/assignments")
def assignments():
    user = session.get('user')
    if not user:
        flash("Please log in to view assignment.", "warning")
        return redirect(url_for('login'))

    uid = user['localId']
    user_data = db.child("users").child(uid).get().val() or {}

    data = db.child("assignments").get().val() or {}
    assignments_data = {}

    for subject, subject_assignments in data.items():
        if isinstance(subject_assignments, dict):
            assignments_data[subject] = [
                {"title": a["title"], "link": a["link"]}
                for a in subject_assignments.values()
            ]

    return render_template("assignment.html", assignments_data=assignments_data, user_data=user_data)




@app.route('/submit_assignment/<subject>/<title>', methods=['POST'])
def submit_assignment(subject, title):
    if 'file' not in request.files:
        flash('No file uploaded', 'danger')
        return redirect(url_for('assignments'))

    file = request.files['file']
    if file.filename == '':
        flash('No file selected', 'danger')
        return redirect(url_for('assignments'))

    # You can store this file in Firebase storage or locally
    storage.child(f"submissions/{subject}/{title}/{file.filename}").put(file)

    flash(f'Submission for "{title}" received successfully!', 'success')
    return redirect(url_for('assignments'))

@app.route("/upload_assignment", methods=["POST"])
def upload_assignment():
    user = session.get('user')
    if not user:
        flash("Please log in first.", "warning")
        return redirect(url_for('login'))

    uid = user['localId']
    user_data = db.child("users").child(uid).get().val() or {}

    # 🛑 Check if the user is a faculty member
    if user_data.get("role") != "faculty":
        flash("Only faculty members can upload assignments!", "danger")
        return redirect(url_for("assignments"))

    subject = request.form["subject"].strip()
    title = request.form["title"]
    pdf_link = request.form["pdf_link"]

    assignments_data = db.child("assignments").get().val() or {}

    # ✅ Append or create subject section
    if subject in assignments_data:
        existing = assignments_data[subject]
        new_key = f"assignment{len(existing) + 1}"
        db.child("assignments").child(subject).child(new_key).set({
            "title": title,
            "link": pdf_link
        })
    else:
        db.child("assignments").child(subject).set({
            "assignment1": {
                "title": title,
                "link": pdf_link
            }
        })

    flash(f"Assignment added under '{subject}' successfully!", "success")
    return redirect(url_for("assignments"))

@app.route("/feedback", methods=["GET", "POST"])
def feedback():
    if request.method == "POST":
        user = request.form["user"]
        text = request.form["feedback"]

        # Automatic sentiment analysis
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        if polarity > 0.2:
            sentiment = "positive"
        elif polarity < -0.2:
            sentiment = "negative"
        else:
            sentiment = "neutral"

        # Store in Firebase with timestamp
        db.child("feedbacks").push({
            "user": user,
            "text": text,
            "sentiment": sentiment,
            "timestamp": datetime.now().isoformat()  # ISO timestamp
        })

        return redirect("/feedback")

    # Fetch all feedbacks
    feedbacks = db.child("feedbacks").get().val()
    feedback_list = []

    if feedbacks:
        for key, val in feedbacks.items():
            feedback_list.append(val)

    # Sort by timestamp (latest first)
    feedback_list.sort(key=lambda x: x.get("timestamp", ""), reverse=True)

    # Filtering by sentiment
    sentiment_filter = request.args.get("filter", "all")
    if sentiment_filter != "all":
        feedback_list = [f for f in feedback_list if f["sentiment"] == sentiment_filter]

    return render_template("feedback.html", feedbacks=feedback_list, selected=sentiment_filter)




if __name__ == '__main__':
    app.run(debug=True)
