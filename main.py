from modules.Data import Data
from modules.FeatureEngineering import FeatureEngineering
import pandas as pd
from sklearn.cluster import KMeans
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()  # for plot styling
from sklearn.decomposition import PCA
import plotly.express as px
import plotly.graph_objects as go
from sklearn.preprocessing import MinMaxScaler
from modules.Clustering import  Clustering
def main():
    # data = Data()

    # featureEngineering = FeatureEngineering(data)

    clustering = Clustering("volatility_df.csv")

if __name__ == "__main__":
    main()

