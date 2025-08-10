# Ingestion Pipeline & Solution Recommender

This directory contains all the code and data needed to:
- Ingest and transform raw JSON data into a unified CSV
- Generate semantic embeddings for solution recommendations
- Expose a simple API for querying similar solutions

## Directory Structure

```
app/ingestion-pipeline/
├── data/                # Raw JSON data and parser
│   ├── parser.py
│   └── *.json
├── csv_data/            # Output CSV file
│   └── solutions.csv
├── chroma_db/           # ChromaDB vector database (auto-generated)
├── venv/                # Python virtual environment (recommended)
├── embedding_pipeline.py# Embedding generation and search logic
├── api_server.py        # FastAPI server for demo/testing
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

## 1. Setup

### Prerequisites
- Python 3.9+
- [pip](https://pip.pypa.io/en/stable/)
- [virtualenv](https://virtualenv.pypa.io/en/latest/) (recommended)
- Docker (optional, for running ChromaDB in a container)
- chroma (client library for ChromaDB)


### Start ChromaDB (optional)
```bash
docker run -v ./chroma-data:/data -p 8000:8000 chromadb/chroma:latest
```
Incase of errors like 'error while creating mount source path', execute the below command:
```bash
chmod -R 777 ./chroma-data
```

### Check records in chroma_db
```bash
chroma browse solutions_product_description --host=http://localhost:8000
```

### Install dependencies
```bash
cd app/ingestion-pipeline
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## 2. Data Ingestion: JSON to CSV

Transform all JSON files in `data/` into a single CSV:
```bash
cd data
python parser.py
```
- Output: `../csv_data/solutions.csv`

## 3. Run the API Server (Demo/Test)

Expose a REST API for querying similar solutions:
```bash
python3 api_server.py
```
- The server will be available at: [http://127.0.0.1:8083](http://127.0.0.1:8000)

### Example API Usage
- **Process embeddings**
  - `POST /process`
- **Search by product:**
  - `GET /search?field=product_description&query=LG%20OLED%20TV&n_results=3`
- **Search by business context:**
  - `GET /search?field=business_context&query=PRODUCT_DEFECT:%20SCREEN_DEAD_PIXELS&n_results=3`
- **Search across all fields:**
  - `GET /search?field=all&query=battery%20issues&n_results=3`

### Example Response
```json
{
  "query": "LG OLED TV",
  "field": "product_description",
  "results": [
    {
      "productDescription": "Samsung Galaxy Tab S9 Ultra",
      "businessIncidentContext": "CUSTOMER_ERROR: INCORRECT_ORDER",
      "solutionType": "PRICE_DISCOUNT",
      "partner_id": "3210987",
      "similarity": 0.4156303,
      "field": "BUSINESS_CONTEXT"
    }
  ]
}
```

## 5. Customization
- Add new JSON files to `data/` and rerun the parser and embedding pipeline.
- Adjust fields or embedding logic in `embedding_pipeline.py` as needed.
- Extend the API in `api_server.py` for more advanced use cases.

## 6. Troubleshooting
- If you change the data, always rerun both the parser and embedding pipeline.
- If you see errors about missing dependencies, ensure your virtual environment is activated and dependencies are installed.

---

**Questions?**
Open an issue or contact the project maintainer. 