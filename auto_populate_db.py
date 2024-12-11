from faker import Faker
import random
from utils.db_utils import get_db_connection
from utils.db_utils import get_db_connection

# Initialize Faker
fake = Faker()

db = get_db_connection()
cursor = db.cursor()

def populate_users(num_users):
    print("Populating Users...")
    users = []
    for _ in range(num_users):
        while True:  # Keep generating until a unique username is found in the database
            username = fake.user_name()
            cursor.execute("SELECT COUNT(*) FROM users WHERE username = %s", (username,))
            if cursor.fetchone()[0] == 0:  # If the username doesn't exist
                break
        password = fake.password()
        email = fake.email()
        users.append((username, password, email))
    
    cursor.executemany(
        "INSERT IGNORE INTO users (username, password, email) VALUES (%s, %s, %s)", users
    )
    
    db.commit()
    print(f"Inserted {len(users)} users.")

# Function to Populate Locations
def populate_locations(num_locations):
    print("Populating Locations...")
    locations = []
    for _ in range(num_locations):
        city = fake.city()
        locations.append((city,))
    
    cursor.executemany(
        "INSERT IGNORE INTO locations (name) VALUES (%s)", locations
    )
    db.commit()
    print(f"Inserted {num_locations} locations.")

# Function to Populate Statuses
def populate_statuses():
    print("Populating Statuses...")
    statuses = [
        ("In Transit",),
        ("Delivered",),
        ("Pending",),
        ("Canceled",)
    ]
    cursor.executemany(
        "INSERT IGNORE INTO statuses (name) VALUES (%s)", statuses
    )
    db.commit()
    print(f"Inserted {len(statuses)} statuses.")

# Function to Populate Shipments
def populate_shipments(num_shipments):
    print("Populating Shipments...")
    cursor.execute("SELECT id FROM users")
    user_ids = [row[0] for row in cursor.fetchall()]
    
    cursor.execute("SELECT id FROM locations")
    location_ids = [row[0] for row in cursor.fetchall()]
    
    cursor.execute("SELECT id FROM statuses")
    status_ids = [row[0] for row in cursor.fetchall()]
    
    shipments = []
    for _ in range(num_shipments):
        tracking_number = fake.uuid4()
        origin_id = random.choice(location_ids)
        destination_id = random.choice(location_ids)
        while origin_id == destination_id:
            destination_id = random.choice(location_ids)  # Ensure origin ≠ destination
        current_location_id = random.choice(location_ids)
        status_id = random.choice(status_ids)
        estimated_delivery = fake.date_between(start_date="+1d", end_date="+30d")
        user_id = random.choice(user_ids)
        shipments.append((tracking_number, origin_id, destination_id, current_location_id, status_id, estimated_delivery, user_id))
    
    cursor.executemany(
        """
        INSERT INTO shipments (tracking_number, origin_id, destination_id, current_location_id, status_id, estimated_delivery, user_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, shipments
    )
    db.commit()
    print(f"Inserted {num_shipments} shipments.")

# Main Execution
if __name__ == "__main__":
    try:
        # Adjust the numbers as needed
        populate_users(30000)        # Populate 30000 users
        populate_locations(175)     # Populate 175 unique locations
        populate_statuses()        # Populate statuses (static values)
        populate_shipments(500000)   # Populate 5000000 shipments
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        db.close()
