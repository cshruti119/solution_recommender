# Recommendation Engine

This module provides the core logic for analyzing complaints and generating solution recommendations based on business context and product descriptions.

## Directory Structure

app/recommendation-engine/
├── venv/                 # Python virtual environment (recommended)
├── complaint_analyzer.py # Analyzes complaints and mapping them to solution types
├── index.py              # FastAPI server for demo/testing
├── reason_type_mapping.json # JSON mapping for business incident reason types
├── requirements.txt     # Python dependencies
└── README.md            # This file

## Setup

1. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm // download spacy model
   ```

2. **Run the FastAPI server**

   ```bash
   uvicorn index:app --reload
   ```

## Usage

- Send a POST request to `/analyze-complaint` with JSON body `{ "sentence": "your complaint text" }`.
- Example using `curl`:

   ```bash
   curl -X POST "http://localhost:8000/analyze-complaint" -H "Content-Type: application/json" -d '{"sentence": "your complaint text"}'
   ```

- Import and use `complaint_analyzer.py` for analyzing complaint data.
- Use the provided JSON mapping files for customizing reason type mappings.

## Requirements

- Python 3.8+
- See `requirements.txt` for required packages.
- Additional: `fastapi`, `uvicorn`

## Notes

- Ensure the data files are present in the expected locations.
- For integration with other modules, refer to the main project README.
