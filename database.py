# db_tool/database.py
import asyncio
import mysql.connector
import psycopg2
import cx_Oracle
import sqlite3
from sqlalchemy import create_engine, MetaData
from pymongo import MongoClient
import boto3
from pyspark.sql import SparkSession
from botocore.exceptions import NoCredentialsError
from aiohttp import ClientSession

class AsyncDatabaseConnection:
    def __init__(self, db_type, user=None, password=None, host=None, port=None, database=None, aws_access_key=None, aws_secret_key=None, region=None):
        self.db_type = db_type
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database
        self.aws_access_key = aws_access_key
        self.aws_secret_key = aws_secret_key
        self.region = region
        self.connection = None
        self.spark_session = None

    async def connect(self):
        try:
            if self.db_type == "mysql":
                self.connection = mysql.connector.connect(
                    user=self.user, 
                    password=self.password, 
                    host=self.host, 
                    port=self.port, 
                    database=self.database
                )
            elif self.db_type == "postgresql":
                self.connection = psycopg2.connect(
                    user=self.user, 
                    password=self.password, 
                    host=self.host, 
                    port=self.port, 
                    database=self.database
                )
            elif self.db_type == "oracle":
                self.connection = cx_Oracle.connect(
                    self.user, 
                    self.password, 
                    f"{self.host}:{self.port}/{self.database}"
                )
            elif self.db_type == "sqlite":
                self.connection = sqlite3.connect(self.database)
            elif self.db_type == "mongodb":
                self.connection = MongoClient(f"mongodb://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}")
            elif self.db_type == "dynamodb":
                self.connection = boto3.resource(
                    'dynamodb',
                    aws_access_key_id=self.aws_access_key,
                    aws_secret_access_key=self.aws_secret_key,
                    region_name=self.region
                )
            elif self.db_type == "spark":
                self.spark_session = SparkSession.builder \
                    .appName("UniversalDBTool") \
                    .config("spark.some.config.option", "some-value") \
                    .getOrCreate()
            else:
                raise ValueError(f"Unsupported database type: {self.db_type}")
        except (mysql.connector.Error, psycopg2.OperationalError, cx_Oracle.DatabaseError, sqlite3.Error, NoCredentialsError) as e:
            raise RuntimeError(f"Database connection failed: {e}")

    async def execute_query(self, query, params=None):
        if self.db_type in ["mysql", "postgresql", "oracle", "sqlite"]:
            cursor = self.connection.cursor()
            cursor.execute(query, params or ())
            return cursor.fetchall()
        elif self.db_type == "mongodb":
            db = self.connection[self.database]
            collection = db[params.get('collection')]
            return collection.find(query)
        elif self.db_type == "dynamodb":
            table = self.connection.Table(params.get('table_name'))
            return table.scan(FilterExpression=query)
        elif self.db_type == "spark":
            return self.spark_session.sql(query).collect()
        else:
            raise ValueError(f"Query execution not supported for database type: {self.db_type}")

    async def close(self):
        if self.connection:
            self.connection.close()
        if self.spark_session:
            self.spark_session.stop()

import time

class AsyncDatabaseConnectionWithRetry(AsyncDatabaseConnection):
    def __init__(self, db_type, retries=3, backoff_factor=0.3, **kwargs):
        super().__init__(db_type, **kwargs)
        self.retries = retries
        self.backoff_factor = backoff_factor

    async def connect(self):
        for attempt in range(self.retries):
            try:
                await super().connect()
                return
            except Exception as e:
                wait = self.backoff_factor * (2 ** attempt)
                print(f"Attempt {attempt + 1} failed: {e}. Retrying in {wait} seconds...")
                time.sleep(wait)
        raise RuntimeError("Maximum retries exceeded. Connection failed.")

