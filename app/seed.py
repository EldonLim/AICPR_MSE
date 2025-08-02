import csv
import sys
from pathlib import Path
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from .models.post import Post, Base

def process_array_field(field_value: str) -> list[str]:
    """Convert comma-separated string to list of strings"""
    if not field_value or field_value.strip() == "":
        return []
    return [item.strip() for item in field_value.split(',') if item.strip()]

def clean_row_keys(row: dict) -> dict:
    """Clean whitespace and BOM from dictionary keys"""
    cleaned = {}
    for key, value in row.items():
        # Remove BOM and whitespace from keys
        clean_key = key.strip().lstrip('\ufeff')
        cleaned[clean_key] = value
    return cleaned

def seed_from_csv(csv_file_path: str):
    """Seed database from CSV file"""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    try:
        print("Clearing existing data...")
        db.query(Post).delete()
        db.commit()
        
        print(f"Reading CSV file: {csv_file_path}")
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            
            records_added = 0
            for row_num, raw_row in enumerate(csv_reader, start=2):
                try:
                    # Clean the row keys to remove any whitespace
                    row = clean_row_keys(raw_row)
                    
                    # Debug: print available keys for first row
                    if row_num == 2:
                        print(f"Available CSV columns: {list(row.keys())}")
                    
                    # Process array fields
                    themes = process_array_field(row.get('themes', ''))
                    tags = process_array_field(row.get('tags', ''))
                    
                    # Create Post object
                    post = Post(
                        course=row['course'].strip(),
                        course_name=row['course_name'].strip(),
                        course_summary=row['course_summary'].strip(),
                        course_description=row['course_description'].strip(),
                        course_url=row['course_url'].strip(),
                        number_of_semester=row['number_of_semester'].strip(),
                        themes=themes,
                        tags=tags
                    )
                    
                    db.add(post)
                    records_added += 1
                    
                    if records_added % 10 == 0:
                        print(f"Processed {records_added} records...")
                        
                except KeyError as e:
                    print(f"Missing column {e} in row {row_num}")
                    print(f"Available columns: {list(row.keys())}")
                    break
                except Exception as e:
                    print(f"Error processing row {row_num}: {e}")
                    continue
            
            db.commit()
            print(f"Successfully seeded {records_added} records!")
            
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python -m app.seed <csv_file_path>")
        sys.exit(1)
    
    csv_file = sys.argv[1]
    if not Path(csv_file).exists():
        print(f"CSV file not found: {csv_file}")
        sys.exit(1)
    
    seed_from_csv(csv_file)