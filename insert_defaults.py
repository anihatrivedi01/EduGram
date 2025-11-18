import firebase_admin
from firebase_admin import credentials, db

# Initialize Firebase
cred = credentials.Certificate('firebase_config.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://edu-platform-91bbd-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

ref = db.reference()

# === COURSES with Units and Quizzes ===
courses = {
    'course1': {
        'title': 'Introduction to Computers',
        'units': {
            'unit1': {
                'title': 'Understanding Computers',
                'text': 'Learn about parts of a computer, their uses, and how they work together.',
                'quiz': {
                    'q1': {
                        'question': 'What does CPU stand for?',
                        'options': ['Central Processing Unit', 'Computer Power Unit', 'Central Program Unit'],
                        'answer': 'Central Processing Unit'
                    },
                    'q2': {
                        'question': 'Which one is an output device?',
                        'options': ['Monitor', 'Keyboard', 'Mouse'],
                        'answer': 'Monitor'
                    }
                }
            },
            'unit2': {
                'title': 'Encoding Schemes And Number Systems',
                'text': 'Introduction to Windows and Android, and their basic functions.',
                'quiz': {
                    'q1': {
                        'question': 'Which software runs the computer hardware?',
                        'options': ['Operating System', 'MS Word', 'Chrome'],
                        'answer': 'Operating System'
                    }
                }
            },
            'unit3': {
                'title': 'Emerging Trends',
                'text': 'Emerging Trends',
            },
            'unit4': {
                'title': 'Introduction to problem Solving',
                'text': 'Introduction to problem Solving',
            },
            'unit5': {
                'title': 'Computer Networks',
                'text': 'Learn about different types of networks and their uses.',
                'quiz': {
                    'q1': {
                        'question': 'What does LAN stand for?',
                        'options': ['Local Area Network', 'Large Area Network', 'Long Area Network'],
                        'answer': 'Local Area Network'
                    }
                }
            },
            'unit6': {
                'title': 'Basic Programming Concepts',
                'text': 'Introduction to programming languages and basic concepts.',
                'quiz': {
                    'q1': {
                        'question': 'Which of the following is a programming language?',
                        'options': ['HTML', 'CSS', 'Python'],
                        'answer': 'Python'
                    }
                }
            }
        }
    },

    'course2': {
        'title': 'History of Indian Art',
        'units': {
            'unit1': {
                'title': 'Overview of Indian Art History',
                'text': 'Survey of major periods in Indian art from prehistoric to medieval times, including key styles and influences.',
                'quiz': {
                    'q1': {
                        'question': 'Which period introduced large rock-cut architecture like Ajanta and Ellora?',
                        'options': ['Maurya period', 'Gupta period', 'Medieval period'],
                        'answer': 'Gupta period'
                    }
                }
            },
            'unit2': {
                'title': 'Classical Sculpture and Temple Architecture',
                'text': 'Study of Indian temple styles (Nagara, Dravida, Vesara), temple sculpture programs, and iconic examples.',
                'quiz': {
                    'q1': {
                        'question': 'Which architectural style is associated with South Indian temples?',
                        'options': ['Nagara', 'Dravida', 'Indo-Islamic'],
                        'answer': 'Dravida'
                    }
                }
            },
            'unit3': {
                'title': 'Painting Traditions: Mughal, Rajput & Pahari',
                'text': 'Examine court painting traditions, characteristic themes, techniques, and notable schools.',
                'quiz': {
                    'q1': {
                        'question': 'Which school is known for refined courtly portraiture and realistic detail?',
                        'options': ['Rajput', 'Mughal', 'Pahari'],
                        'answer': 'Mughal'
                    }
                }
            },
            'unit4': {
                'title': 'Folk, Tribal and Contemporary Practices',
                'text': 'Explore regional folk and tribal arts (e.g., Warli, Madhubani), their social contexts, and modern continuities.',
                'quiz': {
                    'q1': {
                        'question': 'Which of these is a tribal art form from Maharashtra?',
                        'options': ['Madhubani', 'Warli', 'Pattachitra'],
                        'answer': 'Warli'
                    }
                }
            }
        }
    },

    'course3': {
        'title': 'Mathematics for Daily Life',
        'units': {
            'unit1': {
                'title': 'Basic Arithmetic',
                'text': 'Learn addition, subtraction, multiplication, and division.',
                'quiz': {
                    'q1': {
                        'question': 'What is 25 + 17?',
                        'options': ['42', '43', '41'],
                        'answer': '42'
                    }
                }
            },
            'unit2': {
                'title': 'Measurements',
                'text': 'Understanding weights, lengths, and time in daily life.',
                'quiz': {
                    'q1': {
                        'question': 'How many centimeters are there in one meter?',
                        'options': ['10', '100', '1000'],
                        'answer': '100'
                    }
                }
            },
            'unit3': {
                'title': 'Basic Geometry',
                'text': 'Introduction to shapes, areas, and volumes.',
                'quiz': {
                    'q1': {
                        'question': 'What is the area of a rectangle with length 5 and width 3?',
                        'options': ['15', '8', '18'],
                        'answer': '15'
                    }
                }
            },
            'unit4': {
                'title': 'Statistics Basics',
                'text': 'Learn about mean, median, and mode.',
                'quiz': {
                    'q1': {
                        'question': 'What is the mean of the numbers 2, 3, and 10?',
                        'options': ['5', '6', '7'],
                        'answer': '5'
                    }
                }
            }
        }
    },

    'course4': {
        'title': 'Digital Literacy',
        'units': {
            'unit1': {
                'title': 'Using Smartphones Safely',
                'text': 'Learn how to use smartphones responsibly and safely.',
                'quiz': {
                    'q1': {
                        'question': 'Which of these is a safe online practice?',
                        'options': ['Sharing passwords', 'Using strong passwords', 'Clicking all links'],
                        'answer': 'Using strong passwords'
                    }
                }
            },
            'unit2': {
                'title': 'Internet Basics',
                'text': 'Understand how to browse, search, and use the internet effectively.',
                'quiz': {
                    'q1': {
                        'question': 'What does URL stand for?',
                        'options': ['Uniform Resource Locator', 'Universal Research Link', 'User Reference Link'],
                        'answer': 'Uniform Resource Locator'
                    }
                }
            },
            'unit3': {
                'title': 'Social Media Awareness',
                'text': 'Learn about the impact of social media on society.',
                'quiz': {
                    'q1': {
                        'question': 'What is a common risk of social media?',
                        'options': ['Connecting with friends', 'Privacy concerns', 'Sharing photos'],
                        'answer': 'Privacy concerns'
                    }
                }
            },
            'unit4': {
                'title': 'Online Safety and Security',
                'text': 'Understand how to protect personal information online.',
                'quiz': {
                    'q1': {
                        'question': 'What is a strong password?',
                        'options': ['123456', 'password', 'A1b2C3!'],
                        'answer': 'A1b2C3!'
                    }
                }
            }
        }
    },

    'course5': {
        'title': 'Environmental Awareness',
        'units': {
            'unit1': {
                'title': 'Clean and Green',
                'text': 'Learn how trees, waste management, and recycling help our environment.',
                'quiz': {
                    'q1': {
                        'question': 'What should we do with plastic waste?',
                        'options': ['Burn it', 'Recycle it', 'Throw it anywhere'],
                        'answer': 'Recycle it'
                    }
                }
            },
            'unit2': {
                'title': 'Sustainability',
                'text': 'Understanding the importance of saving resources for the future.',
                'quiz': {
                    'q1': {
                        'question': 'Which of these is a renewable resource?',
                        'options': ['Coal', 'Water', 'Petrol'],
                        'answer': 'Water'
                    }
                }
            },
            'unit3': {
                'title': 'Climate Change',
                'text': 'Learn about the causes and effects of climate change.',
                'quiz': {
                    'q1': {
                        'question': 'What is a major cause of climate change?',
                        'options': ['Deforestation', 'Planting trees', 'Recycling'],
                        'answer': 'Deforestation'
                    }
                }
            },
            'unit4': {
                'title': 'Biodiversity',
                'text': 'Understand the importance of biodiversity and conservation.',
                'quiz': {
                    'q1': {
                        'question': 'Why is biodiversity important?',
                        'options': ['It helps ecosystems function', 'It is not important', 'It only benefits humans'],
                        'answer': 'It helps ecosystems function'
                    }
                }
            }
        }
    }
}

# === FACULTIES ===
faculties = {
    'f1': {'name': 'Dr. S. Sharma', 'subject': 'Digital Literacy', 'bio': '20 years of experience teaching rural students.'},
    'f2': {'name': 'Ms. R. Verma', 'subject': 'Mathematics', 'bio': 'Practical math trainer focusing on real-life use.'},
     'f3': {'name': 'Dr. DJ Das', 'subject': 'Computer Fundamentals', 'bio': 'Ex-Employee of Amazon.'},
    'f4': {'name': 'Ms. R. Verma', 'subject': 'History of Indian Art', 'bio': 'Won 3rd prize in National Art and Sclupture Competetion.'}
}


# === Push to Firebase ===
# === Push to Firebase Safely ===
existing_courses = ref.child('courses').get() or {}

for key, new_course in courses.items():
    existing_course = existing_courses.get(key, {})

    # Merge units
    merged_units = existing_course.get("units", {})
    for unit_key, new_unit in new_course.get("units", {}).items():
        existing_unit = merged_units.get(unit_key, {})
        # Add only missing fields (don’t overwrite pdfs/videos)
        for field, value in new_unit.items():
            if field not in existing_unit:
                existing_unit[field] = value
        merged_units[unit_key] = existing_unit

    # Merge the rest of the course data
    merged_course = {**existing_course, **new_course}
    merged_course["units"] = merged_units

    ref.child("courses").child(key).set(merged_course)

# === Faculties (can safely overwrite, since small) ===
ref.child('faculties').update(faculties)

print("🌻 Firebase updated safely! No data lost this time.")

