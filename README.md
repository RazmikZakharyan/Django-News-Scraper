# Django News Scraper

## Overview

This Django project is designed to scrape news articles from the [News.am](https://news.am/) website using Scrapy and Celery. The project is containerized using Docker Compose for easy deployment and management.

## Setup

### Prerequisites

Make sure you have the following installed on your system:

- Docker
- Docker Compose

### Getting Started

1. **Clone the repository:**

    ```bash
    git clone https://github.com/RazmikZakharyan/Django-News-Scraper.git
    ```

2. **Build the Docker containers:**

    ```bash
    docker-compose up --build
    ```

    This command will build and start the Django web server, Celery worker, and other necessary services defined in the `docker-compose.yml` file.

3. **Open your web browser and go to [http://localhost:8000/](http://localhost:8000/) to access the Django admin interface.**
