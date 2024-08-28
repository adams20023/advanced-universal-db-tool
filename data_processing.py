# db_tool/data_processing.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import concurrent.futures
from cryptography.fernet import Fernet

def clean_data(df):
    return df.dropna()

def transform_data(df):
    df['new_column'] = df['existing_column'].apply(lambda x: x * 2)
    return df

def process_data(file_path, operation):
    df = pd.read_csv(file_path)
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        if operation == 'clean':
            future = executor.submit(clean_data, df)
            df = future.result()
            df.to_csv(file_path, index=False)
            print(f"Data cleaned and saved back to {file_path}")
        
        elif operation == 'transform':
            future = executor.submit(transform_data, df)
            df = future.result()
            df.to_csv(file_path, index=False)
            print(f"Data transformed and saved back to {file_path}")
        
        elif operation == 'visualize':
            sns.pairplot(df)
            plt.show()

def generate_key():
    return Fernet.generate_key()

def encrypt_data(df, key):
    cipher = Fernet(key)
    df_encrypted = df.applymap(lambda x: cipher.encrypt(x.encode()).decode() if isinstance(x, str) else x)
    return df_encrypted

def decrypt_data(df, key):
    cipher = Fernet(key)
    df_decrypted = df.applymap(lambda x: cipher.decrypt(x.encode()).decode() if isinstance(x, str) else x)
    return df_decrypted

