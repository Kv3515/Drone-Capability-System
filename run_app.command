#!/bin/bash

# Navigate to the app directory
cd "$(dirname "$0")"

# Run the Streamlit app using pipx
pipx run streamlit run app.py
