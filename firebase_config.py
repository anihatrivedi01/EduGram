import pyrebase

firebaseConfig = {
  "apiKey": "AIzaSyA...your_key...",
  "authDomain": "rural-edu-platform.firebaseapp.com",
  "databaseURL": "https://rural-edu-platform-default-rtdb.firebaseio.com",
  "projectId": "rural-edu-platform",
  "storageBucket": "rural-edu-platform.appspot.com",
  "messagingSenderId": "1234567890",
  "appId": "1:1234567890:web:abcdefghij12345"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()
