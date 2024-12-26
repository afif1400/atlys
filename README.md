# Web Scraper

A FastAPI-based web scraper for dental products from dentalstall.com.

## Prerequisites

- Python 3.8 or higher
- Redis server (optional, for caching)
- pip (Python package manager)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/afif1400/atlys.git
cd atlys
```

2. Create and activate a virtual environment (recommended):

```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On Unix or MacOS
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory with the following variables:

```env
API_TOKEN=random_token
REDIS_HOST=redis_host # example: localhost
REDIS_PASSWORD=your_redis_password
```

## Running the Application

1. Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

The server will start at `http://localhost:8000`

## API Endpoints

### Scrape Products

```
POST /scrape
Header: token: your_secure_token
Query Parameters:
- max_pages: Maximum number of pages to scrape
- proxy: Proxy URL (optional)
```

## Project Structure

```
atlys/
├── app/
│   ├── api/
│   ├── core/
│   ├── models/
│   ├── repository/
│   ├── services/
│   ├── config.py
│   └── main.py
├── requirements.txt
└── .env
```

## Documentation

Once the server is running, you can access:

- API documentation: `http://localhost:8000/docs`

## Notes

- Scraped images are saved in an `images/` directory
- Product data is stored in `db.json`
- Redis is used for caching
