#!/bin/bash
# Script to clean up old data in PostgreSQL

# Set your database connection details
DB_USER="your_username"
DB_NAME="your_database_name"
DB_HOST="localhost"  # Change if necessary
DB_PORT="5432"  # Default PostgreSQL port

# Execute the SQL command
psql -U $DB_USER -d $DB_NAME -h $DB_HOST -p $DB_PORT -c "SELECT delete_old_data();"
