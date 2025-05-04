# 🌟 FoodReview API - README

## 📅 Project Description

You work at FoodReview GmbH, a company that aims to build a platform for sharing restaurant experiences. Your team has been tasked with designing and implementing a simple web API that allows users to add restaurants, submit reviews, and retrieve existing restaurant ratings. The goal is to enable people to discover and evaluate dining options based on honest, community-driven feedback.

Your mission is to create a RESTful API using Flask (Python) that interacts with a PostgreSQL database. Users should be able to register, log in, and perform actions such as adding restaurants and leaving reviews on restaurants added by others.

---

## 🔗 URL
https://flask-personal-website.onrender.com/

---

## 🚀 Technologies Used

* Python
* Flask
* PostgreSQL
* Postman (for API testing)

---

## 🔍 Features

* User Registration and Login
* Add New Restaurants
* Submit Reviews for Restaurants
* Retrieve Restaurant Ratings

---

## 💡 Setup Instructions

1. Clone this repository:

```bash
git clone https://github.com/YOUR_USERNAME/flask_food_review.git
```

2. Navigate into the project directory:

```bash
cd flask_food_review
```

3. Create a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate  # Windows
```

4. Install required packages:

```bash
pip install -r requirements.txt
```

5. Set up PostgreSQL database and environment variables:

```bash
export FLASK_APP=app.py
export DATABASE_URL=postgresql://username:password@localhost/your_database_name
```

6. Run the Flask server:

```bash
flask run
```

---

## 🌐 Deployment

Deployed using Render / Heroku / or your cloud provider of choice.

---

## 🎉 License

This project is licensed under the MIT License.

---
