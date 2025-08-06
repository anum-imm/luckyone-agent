# LuckyOne Agent

LuckyOne Agent is an **AI-powered SQL analytics assistant** built using **FastAPI** and **SQLite (Chinook.db)**.  
It is designed to **query structured data**, **analyze results**, and **generate interactive charts** for business insights — all accessible through a simple API.

---

## Features

- **SQL Querying** – Ask natural language questions and get database results.
- **Automated Analytics** – Summarizes and interprets query results.
- **Chart Generation** – Produces bar charts, line charts, and other visualizations in Base64 format for easy frontend integration.
- **FastAPI Backend** – Lightweight and fast REST API for integration.
- **Docker Support** – Easy containerized deployment.

---

## Project Structure

luckyone-agent/
- ├── backend/ # FastAPI backend
- │ ├── main.py # API entry point
- │ ├── databases/ # SQLite DB and ORM models
- │ ├── tools/ # SQL + analytics utilities
- │ ├── requirements.txt # Python dependencies
- │ └── Dockerfile # Backend Dockerfile
- ├── frontend/ # Frontend (HTML/JS/CSS)
- │ └── index.html
- └── README.md 



## Running Locally (without Docker)
Clone the repository

- git clone https://github.com/yourusername/luckyone-agent.git
- cd luckyone-agent/backend
- Install dependencies
- pip install -r requirements.txt
- Run the backend
- uvicorn main:app --reload --host 0.0.0.0 --port 8000
- Open the frontend
- cd ../frontend
- open index.html   # or open manually in your browser

## Running with Docker (Backend Only)

- 1. Build the Backend Image

cd backend
docker build -t luckyone-backend .

- 2. Run the Backend Container

docker run -p 8000:8000 luckyone-backend

Backend will be available at:

http://localhost:8000