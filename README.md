# 📰 News Aggregator with AI Summarization

[![Docker](https://img.shields.io/badge/docker-ready-blue)](https://hub.docker.com/)
[![Python](https://img.shields.io/badge/python-3.12%2B-blue)](https://www.python.org/)
[![OpenAI Powered](https://img.shields.io/badge/AI-OpenAI_GPT4-brightgreen)](https://platform.openai.com/)

## 🚀 Project Overview

This project is a News Aggregator platform that collects news from various sources and uses AI to generate concise summaries. It features:

- ✅ AI-powered topic classification and tagging
- ✅ Personalized recommendations
- ✅ Email digests
- ✅ Scalable architecture with scheduled ingestion

## ⚙️ Architecture

The platform is composed of several interconnected services:

- **API Service** – FastAPI-based RESTful backend for users and admin interactions.
- **Worker Service** – Celery workers for background processing (summarization, tagging, delivery).
- **Scheduler Service** – Celery Beat for periodic task scheduling.
- **Database** – PostgreSQL for persistent storage of articles and metadata.
- **Cache/Broker** – Redis used for both caching and as the Celery message broker.
- **Data Ingestion** – Airflow orchestrates article extractors via ETL pipelines.

> 🧩 **Note:** Currently, the only supported source is [www.pravda.com.ua](https://www.pravda.com.ua).

---

## 📥 Airflow Extractors

Airflow is responsible for populating the database with articles. Each extractor follows a classic **ETL pipeline**:

1. **Extract**: Fetch articles from RSS feeds or APIs.
2. **Transform**: 
   - Filter out already existing articles.
   - Enrich each article with 5 descriptive tags using OpenAI.
3. **Load**: Save cleaned and tagged articles into the PostgreSQL database.

---

## ⚡ Quick Start

### 🔧 Prerequisites

- Docker + Docker Compose
- GNU Make

### 🏁 Setup & Run

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/news-aggregator.git
   cd news-aggregator
   ```

2. **Start all services:**

   ```bash
   make setup
   ```

3. **Access the services:**

   - API Docs: [http://localhost:8000/docs](http://localhost:8000/docs)
   - Airflow UI: [http://localhost:8080](http://localhost:8080)
   - Flower UI: [http://localhost:5555/](http://localhost:5555/)

---

## 🔐 Airflow Configuration

1. **Set the OpenAI API Key:**

   - Go to the Airflow UI → *Admin* → *Variables*
   - Create a variable named: `openai_api_key`
   - [Get your key here](https://platform.openai.com/)

2. **Connect PostgreSQL to Airflow:**

   - Go to *Admin* → *Connections*
   - Add a connection named `postgres_articles` with your DB credentials.

3. **Add Source Feed URL Variable:**

   - Variable name: `rss_ukrainska_pravda_feed`
   - Value: The RSS feed URL from [www.pravda.com.ua](https://www.pravda.com.ua)

---

## 🪪 License

This project is licensed under the MIT License.
