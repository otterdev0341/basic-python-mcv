import os
from dotenv import load_dotenv
from dataclasses import dataclass

# Load environment variables from the .env file (if present)
load_dotenv()

@dataclass
class DbConfig:
    user: str = os.environ.get("MYSQL_USER", "")
    password: str = os.environ.get("MYSQL_PASSWORD", "")
    host: str = os.environ.get("MYSQL_HOST", "localhost")
    port: int = int(os.environ.get("MYSQL_PORT", 3306))
    database: str = os.environ.get("MYSQL_DATABASE_NAME", "")

    def __post_init__(self):
        # You can add validation here to ensure the required fields are set
        if not self.user or not self.password or not self.database:
            raise ValueError("MYSQL_USER, MYSQL_PASSWORD, and MYSQL_DATABASE_NAME are required.")
