# PS Accounting Sample — Odoo 19 Training Project

A sample Odoo 19 module for accounting-related training by PatSoft.

## Prerequisites

- Docker
- Docker Compose

## Quick Start

1. Start the services:

   docker compose up -d

2. Open http://localhost:8869 and create a new database (check "Load demonstration data").

3. Go to **Apps**, search for **"PS Accounting Sample"**, and click **Install**.

## Services

| Service    | URL / Port        |
|------------|-------------------|
| Odoo       | http://localhost:8869 |
| PostgreSQL | localhost:5443    |

## Stop

    docker compose down

To remove volumes (deletes all data):

    docker compose down -v
