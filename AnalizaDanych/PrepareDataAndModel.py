from pyspark.ml import Pipeline, PipelineModel
from pyspark.ml.classification import RandomForestClassifier as RF
from pyspark.ml.feature import StringIndexer, VectorIndexer, VectorAssembler, SQLTransformer, OneHotEncoder
from pyspark.ml.evaluation import MulticlassClassificationEvaluator, BinaryClassificationEvaluator, RegressionEvaluator
from pyspark.ml.tuning import CrossValidator, ParamGridBuilder
import numpy as np
import functools
import pyspark
from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext, Row
from pyspark import SparkContext, SparkConf
from pyspark.sql.functions import udf, monotonically_increasing_id 
from pyspark.sql.types import IntegerType, StringType
import pyspark.sql.functions as F
from pyspark.ml.regression import LinearRegression, RandomForestRegressor
from pyspark.ml.clustering import KMeans
import json
import socket

from pyspark.ml.linalg import Vectors

conf = SparkConf().setAppName('MyFirstStandaloneApp')
conf.set("spark.network.timeout", "5601s")
conf.set("spark.executor.heartbeatInterval","5600s")
sc = SparkContext(conf=conf)
sqlContext = SQLContext(sc)

def transData(data):
    return data.rdd.map(lambda r: [Vectors.dense(r[:-1]),r[-1]]).toDF(['features','label'])



#tutaj zamień ścieżkę do pliku !!!!--------------------------------------------------------------------------
lines = sc.textFile('Structured_data2')

data = lines.map(lambda line: line.split(";"))
df = data.toDF(['Scrap_date','Scrap_time','Country_from','Country_to','Flight_id','Days','Journey_time','Airline1_There',\
                'Airline1_Back','Airline2_There','Airline2_Back','Price1_There','Price1_Back','Price2_There','Price2_Back',\
                'Depart_hour1_There','Depart_hour1_Back','Depart_hour2_There','Depart_hour2_Back','Depart_from1_There',\
                'Depart_from1_Back','Depart_from2_There','Depart_from2_Back','Arrival_hour1_There','Arrival_hour1_Back',\
                'Arrival_hour2_There','Arrival_hour2_Back','Arrive_to1_There','Arrive_to1_Back','Arrive_to2_There',\
                'Arrive_to2_Back','Full_Price'])

#Tu następuje filtracja z kraju do kraju

rf = RandomForestRegressor()
country_list = ['Austria','Belgium',
                    'Croatia', 'Denmark', 'England',
                    'France', 'Germany', 'Greece', 'Ireland', 'Italy',
                    'Norway', 'Poland',
                    'Portugal', 'Russia', 'Spain']
nazwy = ["Airline1_Back",'Airline2_There','Airline2_Back','Airline1_There']

for country_from in country_list:
    for country_to in country_list:
        try:
            df2 = df.filter(df.Country_from ==country_from).filter(df.Country_to ==country_to)
            df_temp = df2.select(df2.Scrap_time.cast("float"),'Airline1_Back','Airline2_There','Airline2_Back'\
                             ,'Airline1_There',df2.Days.cast("float"),df2.Journey_time.cast("float"), df2.Full_Price.cast("float"))


            for nazwa in nazwy:
                indexer = StringIndexer(inputCol=nazwa,outputCol=nazwa+"Index")
                df_temp = indexer.fit(df_temp).transform(df_temp)

            df_temp = df_temp.select('Airline1_BackIndex','Airline2_ThereIndex','Airline2_BackIndex','Airline1_ThereIndex','Scrap_time',\
                   'Days','Journey_time', 'Full_Price')
            transformed= transData(df_temp)
            featureIndexer = VectorIndexer(inputCol="features", \
                                           outputCol="indexedFeatures",\
                                           maxCategories=10).fit(transformed)

            data = featureIndexer.transform(transformed)

            #licz model 
            pipeline = Pipeline(stages=[featureIndexer, rf])
       
            model = pipeline.fit(data)
            model.save("modele/"+country_from+"_"+country_to)
        except:
            print("Puść jeszcze raz ", country_from," ", country_to)