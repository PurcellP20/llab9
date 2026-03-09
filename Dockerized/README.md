# MDO SQL Injection Challenge

A two-stage SQL injection CTF challenge themed around U.S. Air Force intelligence systems.

## Challenge Overview

**Stage 1: Login Bypass**
- Bypass authentication using SQL injection in the password field
- Solution: `' OR 1=1--`

**Stage 2: Access Restricted Intel**
- Access future intelligence reports that are normally restricted
- Solution: `%') OR scope='future'--`
- Flag location: "CLASSIFIED - Operation STEEL SENTINEL"
- Flag: `FLAG{sql_injection_master_2025}`

## 🐳 Docker Setup (Recommended)

### Prerequisites
- Docker
- Docker Compose

### Quick Start

1. **Clone/download all files into a directory with this structure:**
```
usaf-ctf/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .dockerignore
├── app.py
├── usaf_data_seed.py
├── templates/
│   ├── login.html
│   └── dashboard.html
└── static/
    └── style.css
```

2. **Start the containers:**
```bash
docker-compose up -d
```

3. **Access the application:**
```
http://localhost:5000
```

4. **Stop the containers:**
```bash
docker-compose down
```

5. **Reset the challenge (clear database):**
```bash
docker-compose down -v
docker-compose up -d
```

6. **Reset only the challenge completion status:**
```bash
# Connect to database container
docker-compose exec db psql -U postgres -d intel

# Run this SQL command
UPDATE challenge_status SET completed = FALSE WHERE id = 1;

# Exit psql
\q
```

### Container Details
- **Web Application**: Runs on port 5000
- **PostgreSQL Database**: Runs on port 5432
- **Auto-initialization**: Database is automatically seeded on startup

## 💻 Local Setup (Alternative)

### Prerequisites
- Python 3.11+
- PostgreSQL 15+

### Installation

1. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

2. **Setup PostgreSQL database:**
```bash
# Create database
createdb intel

# Or using psql
psql -U postgres -c "CREATE DATABASE intel;"
```

3. **Initialize the database:**
```bash
python usaf_data_seed.py
```

4. **Run the application:**
```bash
python app.py
```

5. **Access the application:**
```
http://localhost:5000
```

## 📊 Database Contents

- **Users**: 2 accounts (analyst, intel_ops)
- **Intelligence Reports**: 19 total
  - 5 Current (October 2025)
  - 8 Historical (August-September 2025)
  - 6 Future (November 2025 - January 2026) - Contains FLAG
- **Challenge Status**: Tracks if challenge has been completed (persists across sessions)


## Educational Purpose

⚠️ **TRAINING ENVIRONMENT** - This is for educational purposes only. No real data was used.

## Troubleshooting

**Database connection errors:**
```bash
# Check if containers are running
docker-compose ps

# View logs
docker-compose logs web
docker-compose logs db

# Restart containers
docker-compose restart
```

**Port already in use:**
```bash
# Edit docker-compose.yml and change port mappings
# For example, change "5000:5000" to "5001:5000"
```

**Database not initializing:**
```bash
# Force recreation
docker-compose down -v
docker-compose up -d --force-recreate
```

## License

****Educational use only. Not for production deployment.****