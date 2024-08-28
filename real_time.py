from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, IntegerType, StringType

def stream_data(source, processing_logic, format):
    spark = SparkSession.builder \
        .appName("RealTimeDataProcessing") \
        .getOrCreate()

    # Define the schema
    schema = StructType([
        StructField("id", IntegerType(), True),
        StructField("name", StringType(), True),
        StructField("value", IntegerType(), True)
    ])

    stream_df = spark \
        .readStream \
        .format(format) \
        .schema(schema) \
        .load(source)

    processed_df = stream_df.selectExpr(processing_logic)

    query = processed_df \
        .writeStream \
        .outputMode("append") \
        .format("console") \
        .start()

    query.awaitTermination()
    spark.stop()

