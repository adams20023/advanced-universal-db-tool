# db_tool/data_validation.py
import json
import pandas as pd
from jsonschema import validate, ValidationError

def validate_data(data_path, schema_path):
    df = pd.read_csv(data_path)
    with open(schema_path, 'r') as schema_file:
        schema = json.load(schema_file)
    
    errors = []
    for index, row in df.iterrows():
        try:
            validate(instance=row.to_dict(), schema=schema)
        except ValidationError as e:
            errors.append(f"Row {index} failed validation: {e.message}")
    
    if errors:
        print(f"Data validation failed with {len(errors)} errors:")
        for error in errors:
            print(error)
    else:
        print("Data validation passed.")

def validate_and_evolve_schema(data_path, schema_path):
    df = pd.read_csv(data_path)
    with open(schema_path, 'r') as schema_file:
        schema = json.load(schema_file)

    errors = []
    for index, row in df.iterrows():
        try:
            validate(instance=row.to_dict(), schema=schema)
        except ValidationError as e:
            errors.append(f"Row {index} failed validation: {e.message}")
    
    if errors:
        print(f"Data validation failed with {len(errors)} errors:")
        for error in errors:
            print(error)
    else:
        print("Data validation passed.")
        # Logic to handle schema evolution (e.g., adding new columns)
        evolve_schema(df, schema)

def evolve_schema(df, schema):
    # Logic to update the schema based on the new data structure
    # Example: Adding missing columns to the schema
    for column in df.columns:
        if column not in schema.get('properties', {}):
            # Add the new column to the schema
            schema['properties'][column] = {"type": "string"}  # Adjust type as necessary

    # Save the updated schema
    with open(schema_path, 'w') as schema_file:
        json.dump(schema, schema_file, indent=4)

