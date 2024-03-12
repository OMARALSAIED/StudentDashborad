import re

# Function to validate address
def validate_address(address):
    pattern = re.compile("^[A-Za-z0-9]+$")
    return bool(pattern.match(address))

# Function to validate cardID and nationalID as numbers
def validate_numeric_input(input_value):
    return input_value.isdigit()

# Function to validate email format
def validate_email(email):
    pattern = re.compile(r"[^@]+@[^@]+\.[^@]+")
    return bool(pattern.match(email))