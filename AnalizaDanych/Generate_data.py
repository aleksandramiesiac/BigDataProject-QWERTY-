import pyspark
from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext
from pyspark.sql import Row
from pyspark import SparkContext, SparkConf
from pyspark.sql.functions import udf
from pyspark.sql.types import IntegerType, StringType
import pyspark.sql.functions as F
import json
import itertools

conf = SparkConf().setAppName('MyFirstStandaloneApp')
sc = SparkContext(conf=conf)
sc.setLogLevel("ERROR")

filepath = "hdfs:///piotr/Projekt/data/"
flightsRDD = sc.textFile(filepath)
header = flightsRDD.first()
filtered = flightsRDD.filter(lambda line: line != header)
parts = filtered.map(lambda line: line.split(';'))

flights = parts.map(lambda p:
                   Row(Scrap_date = p[0],
                       Scrap_time = p[1],
                       Country_from = p[2],
                       Country_to = p[3],
                       Flight_id = int(p[4]),
                       There_or_Back = p[5],
                       Flight_date = p[6],
                       Airline = p[7],
                       Change = int(p[8]),
                       Price = float(p[9]),
                       Depart_hour = p[10],
                       Depart_from = p[11],
                       Arrival_hour = p[12],
                       Arrive_to = p[13]
                      ))

sqlContext = SQLContext(sc)
dt = sqlContext.createDataFrame(flights)
dt.registerTempTable("flights")

timeFmt1 = "yyyy-MM-dd"
timeFmt2 = "dd/MM/yy"
timeDiff = ((F.unix_timestamp('Flight_date', format=timeFmt2)
            - F.unix_timestamp('Scrap_date', format=timeFmt1)) / (24 * 3600)).cast(IntegerType())
dt = dt.withColumn("Days", timeDiff)

processed = dt

df = processed.groupBy(["Scrap_time", "Country_from", "Country_to", "There_or_Back",
                       "Flight_date", "Airline", "Change", "Depart_hour", "Depart_from",
                       "Arrival_hour", "Arrive_to"]).agg(
                   F.mean(processed.Price).alias('Mean'),
                   F.stddev(processed.Price).alias('Stddev'),
		   F.count('Price').alias('Count'))

df.rdd.map(lambda line: ";".join([unicode(x).encode('utf-8') for x in line])).saveAsTextFile("hdfs:///piotr/Projekt/Statistics")
rdd_header = sc.parallelize([";".join(df.schema.names)])
rdd_header.saveAsTextFile("hdfs:///piotr/Projekt/Statistics_header")