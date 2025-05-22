# News Aggregator with AI Summarization

## Project Overview

This repository contains a News Aggregator platform that collects tech news from various sources and uses AI to provide concise summaries. The system features personalized content recommendations, topic classification, and email digests.

## Architecture

The application consists of several services:
- **API Service**: FastAPI application handling user requests
- **Worker Service**: Celery workers for background tasks
- **Scheduler Service**: Celery Beat for scheduled tasks
- **Database**: PostgreSQL for persistent storage
- **Cache/Broker**: Redis for caching and message broker

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Make

### Setup and Run

1. Clone the repository:
```bash
git clone https://github.com/yourusername/news-aggregator.git
cd news-aggregator
```

2. Start the services:
```bash
make setup
```

3. Access the API documentation:
```
http://localhost:8000/docs
```

#### Setup Airflow
```
http://localhost:8080/
```
1. Setup the `openai_api_key` Variable in airflow, you can get it here:
```
https://platform.openai.com/
```

2. Setup the postgresql connection to the backend DB to save the articles.
3. Setup the extractor urls Variables.
```
Variable name: rss_ukrainska_pravda_feed
Where to get: www.pravda.com.ua 
```

## License

MIT