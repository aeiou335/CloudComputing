# # Add Spark Python Files to Python Path
# import sys
# import os
# SPARK_HOME = "/usr/local/spark-0.9.1" # Set this to wherever you have compiled Spark
# os.environ["SPARK_HOME"] = SPARK_HOME # Add Spark path
# os.environ["SPARK_LOCAL_IP"] = "127.0.0.1" # Set Local IP
# sys.path.append( SPARK_HOME + "/python") # Add python files to Python Path


from pyspark.mllib.classification import LogisticRegressionWithSGD
from pyspark.mllib.regression import LabeledPoint
import numpy as np
from pyspark import SparkConf, SparkContext

def getSparkContext():
    """
    Gets the Spark Context
    """
    conf = (SparkConf()
         .setMaster("local") # run on local
         .setAppName("Logistic Regression") # Name of App
         .set("spark.executor.memory", "1g")) # Set 1 gig of memory
    sc = SparkContext(conf = conf) 
    return sc

def mapper(line):
    """
    Mapper that converts an input line to a feature vector
    """    
    feats = line.strip().split(",")
    # labels must be at the beginning for LRSGD
    label = feats[len(feats) - 1] 
    feats = feats[: len(feats) - 1]
    #feats.insert(0,label)
    features = [ float(feature) for feature in feats ] # need floats
    return LabeledPoint(label, np.array(features))

def sigmoid(Z):
    return 1 / (1 + np.exp(-Z))

def predict(x, w):
    if sigmoid(np.dot(x, w)) > 0.5:
        return 1
    else: return 0

def train(parsedData, iteration):
    w = np.zeros((4,))
    lr = 0.01

    for i in range(1, iteration+1):
        gradient = parsedData.map(lambda point: (point.features * (sigmoid(np.dot(point.features, w)) - point.label))).reduce(lambda x,y: (x+y))
        w = w - lr * gradient
        
        if i % 5 == 0:
            labelsAndPreds = parsedData.map(lambda point: (point.label, predict(point.features, w)))
            trainErr = labelsAndPreds.filter(lambda v: v[0] != v[1]).count() / float(parsedData.count())
            print("Epoch: " + str(i))
            print("My Logistic Regression Training Error = " + str(trainErr))
            print(gradient)
    


sc = getSparkContext()

# Load and parse the data
data = sc.textFile("./data_banknote_authentication.txt")
parsedData = data.map(mapper)

# Train model
train(parsedData, 10)
model = LogisticRegressionWithSGD.train(parsedData, 10)

# Predict the first elem will be actual data and the second 
# item will be the prediction of the model
labelsAndPreds = parsedData.map(lambda point: (point.label, model.predict(point.features)))
# Evaluating the model on training data
trainErr = labelsAndPreds.filter(lambda v: v[0] != v[1]).count() / float(parsedData.count())

# Print some stuff
print("Spark Logistic Regression Training Error = " + str(trainErr))