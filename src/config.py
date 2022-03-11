from os import getenv

from dotenv import load_dotenv


def get_config() -> dict:
    load_dotenv()
    config = {
        "postgres": {
            "provider": "postgres",
            "user": getenv("db_user"),
            "password": getenv("db_password"),
            "host": getenv("db_host"),
            "database": getenv("db_name"),
            "port": getenv("db_port")
        }
    }
    return config