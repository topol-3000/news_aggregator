#!/bin/bash

# ───────────────────────────────────────────────────────────────
# Generate and export AIRFLOW__CORE__FERNET_KEY and AIRFLOW_UID
# ───────────────────────────────────────────────────────────────

# Generate a Fernet key using Python
FERNET_KEY=$(python3 -c 'from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())')
JWT_SECRET=$(python3 -c 'import secrets; print(secrets.token_urlsafe(64))')

# Get current user's UID
AIRFLOW_UID=$(id -u)

echo "✅ Generated and exported:"
echo "  FERNET_KEY=$AIRFLOW__CORE__FERNET_KEY"
echo "  AIRFLOW_UID=AIRFLOW_UID"
echo "  JWT_SECRET=$JWT_SECRET"

echo "FERNET_KEY=$FERNET_KEY" >> .env
echo "AIRFLOW_UID=$AIRFLOW_UID" >> .env
echo "JWT_SECRET=$JWT_SECRET" >> .env
echo "✅ Appended to .env"

