#!/usr/bin/env python3
"""
Database setup script for MIZU Sensor Hub.

This script helps users set up the PostgreSQL database and run
initial migrations for the sensor data storage.
"""

import os
import sys
import subprocess
from config import DATABASE_CONFIG, DATABASE_URL_TEMPLATE


def check_postgresql_installed():
    """Check if PostgreSQL is installed and accessible."""
    try:
        result = subprocess.run(['psql', '--version'],
                              capture_output=True, text=True, check=True)
        print(f"PostgreSQL found: {result.stdout.strip()}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("PostgreSQL not found. Please install PostgreSQL first.")
        return False


def create_database():
    """Create the database if it doesn't exist."""
    try:
        # First, drop the database if it exists (for fresh setup)
        drop_db_cmd = [
            'psql', '-h', DATABASE_CONFIG['host'],
            '-p', str(DATABASE_CONFIG['port']),
            '-U', DATABASE_CONFIG['username'],
            '-c', f"DROP DATABASE IF EXISTS {DATABASE_CONFIG['database']};"
        ]

        # Set password environment variable
        env = os.environ.copy()
        env['PGPASSWORD'] = DATABASE_CONFIG['password']

        # Drop existing database
        drop_result = subprocess.run(drop_db_cmd, env=env,
                                   capture_output=True, text=True)

        if drop_result.returncode == 0:
            print(f"Dropped existing database '{DATABASE_CONFIG['database']}' for fresh setup.")
        else:
            print(f"Note: {drop_result.stderr}")

        # Create new database using template0 to avoid collation issues
        create_db_cmd = [
            'psql', '-h', DATABASE_CONFIG['host'],
            '-p', str(DATABASE_CONFIG['port']),
            '-U', DATABASE_CONFIG['username'],
            '-c', f"CREATE DATABASE {DATABASE_CONFIG['database']} TEMPLATE template0;"
        ]

        result = subprocess.run(create_db_cmd, env=env,
                              capture_output=True, text=True)

        if result.returncode == 0:
            print(f"Database '{DATABASE_CONFIG['database']}' created successfully using template0.")
            return True
        else:
            print(f"Failed to create database: {result.stderr}")
            # Try alternative approach if the first one fails
            return create_database_alternative()

    except Exception as e:
        print(f"Error creating database: {e}")
        return False


def create_database_alternative():
    """Alternative method to create database using createdb command."""
    try:
        # Use createdb command which might handle collation issues better
        create_db_cmd = [
            'createdb', '-h', DATABASE_CONFIG['host'],
            '-p', str(DATABASE_CONFIG['port']),
            '-U', DATABASE_CONFIG['username'],
            '--template=template0',
            DATABASE_CONFIG['database']
        ]

        # Set password environment variable
        env = os.environ.copy()
        env['PGPASSWORD'] = DATABASE_CONFIG['password']

        result = subprocess.run(create_db_cmd, env=env,
                              capture_output=True, text=True)

        if result.returncode == 0:
            print(f"Database '{DATABASE_CONFIG['database']}' created successfully using createdb.")
            return True
        else:
            print(f"Alternative database creation failed: {result.stderr}")
            return False

    except Exception as e:
        print(f"Error in alternative database creation: {e}")
        return False


def run_migrations():
    """Run Alembic migrations to create tables."""
    try:
        # Update alembic.ini with the correct database URL
        database_url = DATABASE_URL_TEMPLATE.format(**DATABASE_CONFIG)

        # Run alembic upgrade
        result = subprocess.run(['alembic', 'upgrade', 'head'],
                              capture_output=True, text=True, check=True)
        print("Migrations completed successfully.")
        print(result.stdout)
        return True

    except subprocess.CalledProcessError as e:
        print(f"Migration failed: {e.stderr}")
        return False
    except Exception as e:
        print(f"Error running migrations: {e}")
        return False


def test_database_connection():
    """Test the database connection."""
    try:
        from database_models import init_database
        database_url = DATABASE_URL_TEMPLATE.format(**DATABASE_CONFIG)
        init_database(database_url)
        print("Database connection test successful.")
        return True
    except Exception as e:
        print(f"Database connection test failed: {e}")
        return False


def main():
    """Main setup function."""
    print("MIZU Sensor Hub Database Setup")
    print("=" * 40)

    # Check PostgreSQL installation
    if not check_postgresql_installed():
        print("\nPlease install PostgreSQL and ensure 'psql' is in your PATH.")
        print("Download from: https://www.postgresql.org/download/")
        return False

    print(f"\nDatabase configuration:")
    print(f"  Host: {DATABASE_CONFIG['host']}")
    print(f"  Port: {DATABASE_CONFIG['port']}")
    print(f"  Database: {DATABASE_CONFIG['database']}")
    print(f"  Username: {DATABASE_CONFIG['username']}")

    # Ask user to confirm configuration
    response = input("\nDo you want to proceed with this configuration? (y/n): ")
    if response.lower() != 'y':
        print("Setup cancelled.")
        return False

    # Create database
    print("\nCreating database...")
    if not create_database():
        print("Failed to create database. Please check your PostgreSQL configuration.")
        return False

    # Run migrations
    print("\nRunning database migrations...")
    if not run_migrations():
        print("Failed to run migrations. Please check the error messages above.")
        return False

    # Test connection
    print("\nTesting database connection...")
    if not test_database_connection():
        print("Database connection test failed.")
        return False

    print("\n" + "=" * 40)
    print("Database setup completed successfully!")
    print("You can now run the MIZU Sensor Hub application.")
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
