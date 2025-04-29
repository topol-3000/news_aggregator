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
- Make (optional, for using the Makefile commands)

### Setup and Run

1. Clone the repository:
```bash
git clone https://github.com/yourusername/news-aggregator.git
cd news-aggregator
```

2. Start the services:
```bash
make build-up
```

3. Access the API documentation:
```
http://localhost:8000/docs
```


## License

MIT