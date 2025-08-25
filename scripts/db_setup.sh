#!/bin/sh

export PGUSER="${USER_NAME}"
export PGPASSWORD="${POSTGRES_PASSWORD}"

psql postgres -c "CREATE DATABASE social_db"
psql social_db -c "CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";"


