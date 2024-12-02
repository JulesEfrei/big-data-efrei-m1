import os

# Global variables
REGIONS = ["euw1", "jp1", "kr"]
RATE_LIMIT_CALLS = 20
RATE_LIMIT_WINDOW = 1  # in seconds
OUTPUT_PATH_ROOT = "./data/bronze/"
API_KEY = "RGAPI-94857acb-4833-42a4-a11f-5231e46c6e74"

# Function to create directories if they don't exist
def create_directories():
    paths = [
        OUTPUT_PATH_ROOT,
        "./data/silver",
        "./data/gold"
    ]

    # Create main directories
    for path in paths:
        os.makedirs(path, exist_ok=True)

if __name__ == "__main__":
    create_directories()
    print("Directories created successfully.")