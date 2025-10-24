# Trancendos Ecosystem

## Financial Autonomy Platform with AI-Powered Scalability

Welcome to the Trancendos Ecosystem, a comprehensive fintech platform featuring the Alervato financial management system and the Luminous-MastermindAI analytics engine. This repository contains the full source code and infrastructure configuration for a production-ready, enterprise-grade financial application.

## Architecture Overview

The Trancendos Ecosystem is built on a microservices architecture, orchestrated with Docker Compose. The core components are:

-   **Frontend**: A modern React application that serves as the user interface for the platform.
-   **Java Backend (`backend-java`)**: A Spring Boot application responsible for core financial management, transaction processing, and user authentication.
-   **Python Backend (`backend-python`)**: A FastAPI application that powers the Luminous-MastermindAI features, including financial analytics, predictions, and insights.
-   **PostgreSQL (`postgres`)**: The primary relational database for storing user data and financial transactions.
-   **Redis (`redis`)**: An in-memory data store used for caching and session management to improve performance.
-   **Nginx (`nginx`)**: A reverse proxy that routes incoming traffic to the appropriate frontend or backend service.
-   **Prometheus & Grafana**: A monitoring stack for collecting metrics and visualizing system health and performance.

### Technology Stack

-   **Frontend**: React, Redux, Material-UI
-   **Backend**: Java (Spring Boot), Python (FastAPI)
-   **Database**: PostgreSQL, Redis
-   **Infrastructure**: Docker, Docker Compose, Nginx
-   **Monitoring**: Prometheus, Grafana

## Getting Started

Follow these instructions to set up and run the Trancendos Ecosystem on your local machine.

### Prerequisites

-   [Docker](https://www.docker.com/get-started) and [Docker Compose](https://docs.docker.com/compose/install/) are the **only** requirements. You do not need to install Node.js, Java, or Python on your host machine, as all services run inside isolated Docker containers.

### Development Setup

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/Trancendos/trancendos-ecosystem.git
    cd trancendos-ecosystem
    ```

2.  **Configure Environment Variables**
    The application uses a `.env` file to manage sensitive configuration. Start by copying the example file:
    ```bash
    cp .env.example .env
    ```
    Now, open the `.env` file and set the required passwords for the PostgreSQL database and Grafana:
    ```
    POSTGRES_PASSWORD=your_strong_postgres_password
    GRAFANA_PASSWORD=your_strong_grafana_admin_password
    ```

3.  **Build and Run the Application**
    Use Docker Compose to build the images and start all the services:
    ```bash
    docker-compose up --build
    ```
    This command will build the Docker images for the frontend and backend services and start all containers. It may take some time on the first run.

4.  **Access the Services**
    Once all services are running, you can access them at the following local addresses:
    -   **Frontend Application**: [http://localhost:3000](http://localhost:3000)
    -   **Grafana Dashboard**: [http://localhost:3001](http://localhost:3001) (log in with `admin` and the password you set in the `.env` file)
    -   **Prometheus Metrics**: [http://localhost:9090](http://localhost:9090)

## Security Notice

This application handles sensitive financial data and is designed with strict security measures in mind:
-   All API endpoints are intended to be authenticated and rate-limited in a production environment.
-   Data is encrypted in transit and at rest.
-   The codebase includes comprehensive audit logging and compliance checks.

## Documentation

All documentation is embedded directly within the source code, following standard conventions for each programming language (JSDoc, Javadoc, and Google Style Python Docstrings). This ensures that the documentation is always up-to-date with the code.

## License

Proprietary - All rights reserved

## Contact

For security issues or compliance questions, please contact: [security@trancendos.com](mailto:security@trancendos.com)
