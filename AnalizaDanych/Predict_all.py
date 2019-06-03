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
import pandas as pd

from pyspark.ml.linalg import Vectors

conf = SparkConf().setAppName('MyFirstStandaloneApp')
conf.set("spark.network.timeout", "5601s")
conf.set("spark.executor.heartbeatInterval","5600s")
sc = SparkContext(conf=conf)
sqlContext = SQLContext(sc)

def transData(data):
    return data.rdd.map(lambda r: [Vectors.dense(r[:-1]),r[-1]]).toDF(['features','label'])



#----------ZMIEŃ ŚCIEŻKĘ DO PLIKU Z DANYMI TRENINGOWYMI!!!!---------------
lines = sc.textFile('Structured_data2')
data = lines.map(lambda line: line.split(";"))
df = data.toDF(['Scrap_date','Scrap_time','Country_from','Country_to','Flight_id','Days','Journey_time','Airline1_There',\
                'Airline1_Back','Airline2_There','Airline2_Back','Price1_There','Price1_Back','Price2_There','Price2_Back',\
                'Depart_hour1_There','Depart_hour1_Back','Depart_hour2_There','Depart_hour2_Back','Depart_from1_There',\
                'Depart_from1_Back','Depart_from2_There','Depart_from2_Back','Arrival_hour1_There','Arrival_hour1_Back',\
                'Arrival_hour2_There','Arrival_hour2_Back','Arrive_to1_There','Arrive_to1_Back','Arrive_to2_There',\
                'Arrive_to2_Back','Full_Price'])


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
            nazwy_Airline2_There = list(df2.toPandas()['Airline2_There'].unique())
            nazwa_days = list(df2.toPandas()['Days'].unique())
            nazwa_Journey_time = list(df2.toPandas()['Journey_time'].unique())
            nazwa_time = ['2','20']
            
            l = []
            i = 0 


            for nazwa4 in nazwy_Airline2_There:
                for nazwa5 in nazwa_time:
                    for days in nazwa_days:
                        for journey in nazwa_Journey_time:

                            l.append([nazwa5,nazwa4, nazwa4, nazwa4, nazwa4, days, journey, i ])
                            i+=1
            df = pd.DataFrame(l, columns = ['Scrap_time','Airline1_There',\
                             'Airline1_Back','Airline2_There','Airline2_Back','Days','Journey_time','Full_Price']) 
            spark_df = sqlContext.createDataFrame(df)
            
            
            df_temp = spark_df.select(spark_df.Scrap_time.cast("float"),'Airline1_Back','Airline2_There','Airline2_Back'\
                         ,'Airline1_There',spark_df.Days.cast("float"),spark_df.Journey_time.cast("float"),\
                                      spark_df.Full_Price.cast("float"))
            temp2 = df_temp
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
#---------TUTAJ ŚCIEŻKA DO PLIKU Z MODELAMI !!!
            model = PipelineModel.load("modele\\"+country_from+"_"+country_to)
            
            predictions = model.transform(data)
            
            pred = predictions.select(predictions.label.cast("float"),'prediction')
            ta = temp2.alias('ta')
            tb = pred.alias('tb')
            inner_join = ta.join(tb, ta.Full_Price == tb.label).select(['Scrap_time','Airline1_Back','Airline2_There','Airline2_Back',\
                                                            'Airline1_There','Days','Journey_time','prediction'])
# ------------------TUTAJ ŚCIEŻKA DO FOLDERU PREDICTED !!!!!!!!!!!!!
            inner_join.toPandas().to_csv('predicted\\'+country_from+"_"+country_to+'.csv')
        except:
            print("coś poszło nie tak :( ")
