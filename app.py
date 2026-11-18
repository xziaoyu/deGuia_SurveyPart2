from database import create_db_and_tables
from models import User  # Load the User table before creating the database.


def main():
    create_db_and_tables()
    print("User table is ready.")


if __name__ == "__main__":
    main()