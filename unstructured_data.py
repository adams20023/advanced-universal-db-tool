# db_tool/unstructured_data.py
from PIL import Image
import pytesseract

def process_unstructured_data(file_path, data_type):
    if data_type == "text":
        with open(file_path, 'r') as file:
            data = file.read()
        print("Text Data:", data)
    
    elif data_type == "image":
        image = Image.open(file_path)
        text = pytesseract.image_to_string(image)
        print("Extracted Text from Image:", text)

    # Add more unstructured data types as needed (e.g., audio, video)
    print("Unstructured data processing completed.")

