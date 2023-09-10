#!/bin/bash

current_dir=$(pwd)

# Start the frontend in the background
cd "${current_dir}/chat-langchain"
yarn dev &

# Start the backend in the foreground
cd "${current_dir}"
python3 main.py
