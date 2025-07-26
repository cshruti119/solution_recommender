import json
import csv
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional


def parse_date(date_obj: Any) -> Optional[str]:
    """
    Parse date objects from MongoDB format to timestamp (seconds since epoch).
    Handles both timestamp and ISO string formats.
    """
    if not date_obj:
        return None
    
    # Handle MongoDB date format with $date
    if isinstance(date_obj, dict) and '$date' in date_obj:
        date_value = date_obj['$date']
        if isinstance(date_value, dict) and '$numberLong' in date_value:
            # Timestamp in milliseconds, convert to seconds
            timestamp_ms = int(date_value['$numberLong'])
            return str(timestamp_ms // 1000)
        elif isinstance(date_value, str):
            # ISO string format, parse and convert to timestamp
            try:
                dt = datetime.fromisoformat(date_value.replace('Z', '+00:00'))
                return str(int(dt.timestamp()))
            except ValueError:
                return str(date_value)
        else:
            return str(date_value)
    
    # Handle direct timestamp (assume milliseconds if large number)
    elif isinstance(date_obj, (int, float)):
        if date_obj > 1e12:  # Likely milliseconds
            return str(int(date_obj // 1000))
        else:  # Likely seconds
            return str(int(date_obj))
    elif isinstance(date_obj, str):
        # Try to parse ISO string
        try:
            dt = datetime.fromisoformat(date_obj.replace('Z', '+00:00'))
            return str(int(dt.timestamp()))
        except ValueError:
            return date_obj
    
    return str(date_obj)


def extract_solution_type(solutions: List[Dict]) -> Optional[str]:
    """
    Extract solution type from solutions array.
    Look for _class field or other indicators of solution type.
    """
    if not solutions:
        return None
    
    # Get the first solution's class
    first_solution = solutions[0]
    return first_solution.get('_class', 'UNKNOWN')


def extract_fields_from_record(record: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract the required fields from a single record.
    """
    extracted = {}
    
    # Extract createdAt
    extracted['createdAt'] = parse_date(record.get('createdAt'))
    
    # Extract productId (may not exist in all records)
    extracted['productId'] = record.get('productId', '')
    
    # Extract productDescription
    extracted['productDescription'] = record.get('productDescription', '')
    
    # Extract solutionType from solutions array
    solutions = record.get('solutions', [])
    extracted['solutionType'] = extract_solution_type(solutions)
    
    # Extract problemDetail fields
    problem_detail = record.get('problemDetail', {})
    extracted['businessIncidentReasonType'] = problem_detail.get('businessIncidentReasonType', '')
    extracted['businessIncidentReason'] = problem_detail.get('businessIncidentReason', '')
    
    # Extract partner._id
    partner = record.get('partner', {})
    extracted['partner_id'] = partner.get('_id', '')
    
    return extracted


def process_json_file(file_path: Path) -> List[Dict[str, Any]]:
    """
    Process a single JSON file and return extracted records.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if not isinstance(data, list):
            print(f"Warning: {file_path.name} does not contain a list of records")
            return []
        
        extracted_records = []
        for record in data:
            if isinstance(record, dict):
                extracted_record = extract_fields_from_record(record)
                extracted_records.append(extracted_record)
        
        print(f"Processed {len(extracted_records)} records from {file_path.name}")
        return extracted_records
    
    except Exception as e:
        print(f"Error processing {file_path.name}: {str(e)}")
        return []


def create_output_directory(output_dir: Path) -> None:
    """
    Create output directory if it doesn't exist.
    """
    output_dir.mkdir(parents=True, exist_ok=True)


def write_csv(records: List[Dict[str, Any]], output_path: Path) -> None:
    """
    Write records to CSV file.
    """
    if not records:
        print("No records to write to CSV")
        return
    
    fieldnames = [
        'createdAt',
        'productId', 
        'productDescription',
        'solutionType',
        'businessIncidentReasonType',
        'businessIncidentReason',
        'partner_id'
    ]
    
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)
    
    print(f"Successfully wrote {len(records)} records to {output_path}")


def main():
    """
    Main pipeline function that processes all JSON files and creates a combined CSV.
    """
    # Define paths
    current_dir = Path(__file__).parent
    data_dir = current_dir  # Now we're already in the data directory
    output_dir = current_dir.parent / 'csv_data'  # Go up one level to get to csv_data
    output_file = output_dir / 'solutions.csv'
    
    # Create output directory
    create_output_directory(output_dir)
    
    # Check if data directory exists
    if not data_dir.exists():
        print(f"Error: Data directory {data_dir} does not exist")
        return
    
    # Find all JSON files
    json_files = list(data_dir.glob('*.json'))
    
    if not json_files:
        print(f"No JSON files found in {data_dir}")
        return
    
    print(f"Found {len(json_files)} JSON files to process")
    
    # Process all JSON files
    all_records = []
    for json_file in json_files:
        records = process_json_file(json_file)
        all_records.extend(records)
    
    # Write combined CSV
    if all_records:
        write_csv(all_records, output_file)
        print(f"\nPipeline completed successfully!")
        print(f"Total records processed: {len(all_records)}")
        print(f"Output file: {output_file}")
    else:
        print("No records were extracted from the JSON files")


if __name__ == "__main__":
    main()
