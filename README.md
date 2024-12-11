# Shipment Tracking System

## Overview
This project is a **shipment tracking system** that allows users to manage and track shipments efficiently. It includes features for managing users, locations, shipment statuses, and predictive analytics for canceled shipments based on historical data.

The system is built with **Python**, **MySQL**, and integrates machine learning for predictive insights.

---

## Features

### Core Features:
- **User Management**: Add, update, and remove users.
- **Shipment Tracking**: Track shipments with real-time status updates.
- **Location Management**: Manage origin, destination, and current location data.
- **Shipment Status**: Monitor shipment progress (e.g., `In Transit`, `Delivered`, `Canceled`).

### Predictive Analytics:
- Predict the likelihood of shipment cancellations using historical data.
- Analyze patterns using advanced machine learning models.

### Data Population:
- Automatically populate the database with realistic test data for users, locations, statuses, and shipments using the `auto_populate_db.py` script.

---

## Installation

### Prerequisites:
- Python 3.8+
- MySQL 8.0+
- Virtual environment (recommended)

### Steps:

1. Clone the repository:
   ```bash
   git clone git clone https://github.com/ShardulLeo/Shipment_Tracking.git
   cd Shipment_Tracking
   ```

2. Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # For Linux/MacOS
   venv\Scripts\activate   # For Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure the database:
   - Create a MySQL database (e.g., `shipment_tracking`).
   - Import the database schema using the `schema.sql` file:
     ```bash
     mysql -u root -p shipment_tracking < schema.sql
     ```

5. Update the database connection in `config.py`:
   ```python
   DB_HOST = 'localhost'
   DB_USER = 'your_username'
   DB_PASSWORD = 'your_password'
   DB_NAME = 'shipment_tracking'
   ```

6. Populate the database with test data:
   Run the `auto_populate_db.py` script to add sample users, locations, statuses, and shipments.
   ```bash
   python auto_populate_db.py
   ```

7. Run the application:
   ```bash
   python app.py
   ```

---

## Machine Learning Model

The project includes a machine learning model to predict shipment cancellations.

### Steps:

1. Prepare the dataset:
   - Export shipment data from the database.
   - Save it as a CSV file (e.g., `shipments.csv`).

2. Train the model:
   ```bash
   python train_model.py
   ```

3. Save the trained model:
   The model is saved as `cancellation_model.pkl`.

4. Use the model:
   The trained model can be used for real-time predictions in the application.

---

## Directory Structure
```
shipment-tracking/
├── app.py                  # Main application file
├── config.py               # Database configuration
├── schema.sql              # Database schema
├── requirements.txt        # Python dependencies
├── data/
│   └── shipments.csv       # Dataset for training
├── models/
│   └── cancellation_model.pkl  # Trained machine learning model
├── utils/
│   └── db_utils.py         # Database helper functions
├── static/
│   └── styles.css          # Static files (CSS/JS)
├── templates/
│   └── index.html          # HTML templates
├── auto_populate_db.py     # Script to populate database
├── train_model.py          # Script to train the ML model
└── README.md               # Project documentation
```
