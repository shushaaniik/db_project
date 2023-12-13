import requests
import random
from faker import Faker
from datetime import date  # Import the date module

fake = Faker()

base_url = "http://127.0.0.1:8000"

# Function to create a random ConnectionOperator
def create_random_operator():
    operator_data = {
        "name": fake.company(),
        "number_count": random.randint(1, 100)
    }
    response = requests.post(f"{base_url}/operators/", json=operator_data)
    return response.json()

# Function to create a random Subscriber
def create_random_subscriber():
    subscriber_data = {
        "passport_data": fake.uuid4(),
        "name": fake.first_name(),
        "surname": fake.last_name(),
        "address": fake.address()
    }
    response = requests.post(f"{base_url}/subscribers/", json=subscriber_data)
    return response.json()

# Function to create a random Connection
def create_random_connection(operator_code: int, passport_data: str):
    connection_data = {
        "operator_code": operator_code,
        "passport_data": passport_data,
        "number": fake.phone_number(),
        "tarif_plan": fake.word(),
        "set_date": str(fake.date_this_decade()),  # Convert the date to a string
        "price": round(random.uniform(10.0, 100.0), 2)
    }
    response = requests.post(f"{base_url}/connections/", json=connection_data)
    return response.json()

# Number of records to create
num_records = 100

for _ in range(num_records):
    # Create random ConnectionOperators
    operator = create_random_operator()
    operator_code = operator.get("operator_code", None)

    # Create random Subscribers
    subscriber = create_random_subscriber()
    passport_data = subscriber.get("passport_data", None)

    # Create random Connections
    create_random_connection(operator_code, passport_data)

print("Data population complete.")
