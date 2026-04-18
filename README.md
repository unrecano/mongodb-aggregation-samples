# Platzi MongoDB Aggregation Framework Course

This repository contains the exercises, scripts, and sample data for the **MongoDB Aggregation Framework** course from [Platzi](https://platzi.com/). It demonstrates how to effectively use various aggregation pipeline stages using Python (`pymongo`).

## Project Structure

```text
.
├── .env.example            # Environment variables template
├── docker-compose.yml      # Docker Compose configuration for the MongoDB database
├── README.md               # This file
├── requirements.txt        # Python dependencies
├── data/                   # JSON sample datasets (Airbnb, Analytics, Supplies)
├── docs/                   # Additional documentation
├── local/                  # Initialization scripts for the Docker container
└── src/                    # Source code
    ├── db.py               # MongoDB connection context manager
    └── operators/          # Python scripts demonstrating different aggregation operators
        ├── geo_near.py
        ├── group.py
        ├── lookup.py
        ├── match.py
        ├── out.py
        ├── project.py
        ├── set.py
        ├── sum_and_avg.py
        └── unwind.py
```

## Prerequisites

Before running the project, make sure you have the following installed:
- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/)
- Python 3.8+

## Setup Instructions

Follow these steps to set up the project locally:

### 1. Set Up the Environment Variables
Copy the `.env.example` file to create your own `.env` configuration file:
```bash
cp .env.example .env
```

### 2. Start the Database
Start the MongoDB database using Docker. The initialization scripts will automatically import the datasets found in the `data/` folder into the database (this may take a couple of minutes):
```bash
docker compose up -d
```
*Wait a moment for `mongoimport` to finish loading the sample data before proceeding.*

### 3. Set Up the Python Environment
It is highly recommended to use a virtual environment to manage dependencies:
```bash
# Create the virtual environment
python -m venv venv

# Activate the virtual environment
source venv/bin/activate  # On macOS/Linux
# venv\Scripts\activate   # On Windows

# Install the required packages
pip install -r requirements.txt
```

## Running the Examples

Once the database is up and the Python dependencies are installed, you can execute any of the operator scripts directly from the root of the project.

Each script connects to the database, runs a specific aggregation pipeline, and prints the result to the console.

**Examples:**
```bash
python -m src.operators.match
python -m src.operators.group
python -m src.operators.sum_and_avg
python -m src.operators.unwind
```

Feel free to modify the pipelines inside `src/operators/` to experiment with your own aggregations!
