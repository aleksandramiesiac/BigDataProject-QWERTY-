import pyspark
from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext
from pyspark.sql import Row
from pyspark import SparkContext, SparkConf
from pyspark.sql.functions import udf
from pyspark.sql.types import IntegerType, StringType
import pyspark.sql.functions as F
import json

conf = SparkConf().setAppName('MyFirstStandaloneApp')
sc = SparkContext(conf=conf)

filepath = "./flights_reduces.text "

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
                       Flight_date = p[5],
                       Airline = p[6],
                       Change = int(p[7]),
                       Price = float(p[8]),
                       Depart_hour = p[9],
                       Depart_from = p[10],
                       Arrival_hour = p[11],
                       Arrive_to = p[12]
                      ))

sqlContext = SQLContext(sc)
dt = sqlContext.createDataFrame(flights)
dt = dt.withColumn("Days", F.datediff(F.to_date(F.unix_timestamp( dt.Flight_date, "dd/MM/yy").cast("timestamp")), 
                                    F.to_date(F.unix_timestamp( dt.Scrap_date, "'yyyy-MM-dd").cast("timestamp"))))
dt = dt.withColumn("Direction", F.lit('There'))
dt.registerTempTable("flights")

direction = 'There'
country_from = 'Austria'
country_to = 'Bulgaria'
scrap_time = '05:00'

query = "SELECT * FROM flights WHERE Country_from = '{0}' AND Country_to = '{1}' \
AND Scrap_time = '{2}' AND Direction = '{3}'".format(country_from, country_to, scrap_time, direction)

processed = sqlContext.sql(query)
price_sum = processed.agg(F.sum(processed.Price).alias('Price_sum')) 
price_sum.rdd.map(lambda x: x).saveAsTextFile('Price_sum.csv')
#price_sum.write.format('com.databricks.spark.csv').save('Price_sum.csv')