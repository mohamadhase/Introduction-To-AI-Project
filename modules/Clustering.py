from isort import file
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
import plotly.graph_objects as go
import plotly.express as px
from sklearn.decomposition import PCA
import seaborn as sns
from yaml import ScalarNode; sns.set()  # for plot styling
import matplotlib.pyplot as plt

class Clustering:
    def __init__(self,file_name):
        self.df = self.read_data(file_name)
        self.cleaned_data = self.data_cleaning()
        self.scaled_data = self.scaling_data()
        self.elbow_method()
        self.optimal_K = 3
        self.clusters = self.clustering()
        self.pi_ploting()
        self.polar_ploting()
        self.saving_data()
    def read_data(self,file_name):
        data =  pd.read_csv(file_name)
        data = data[data["DV1"]!=0]
        data = data[data["DV2"]!=0]
        return data



    def data_cleaning(self):
        new_df = self.df.copy(deep=True)
        new_df= new_df.replace([np.inf, -np.inf], np.nan)
        new_df = new_df.dropna()
        new_df = new_df.reset_index()
        new_df =  new_df.drop(["trackId","recordingId","index"],axis=1)
        return new_df


    def scaling_data(self):
        scaler = MinMaxScaler()
        scaler.fit(self.cleaned_data)
        return scaler.transform(self.cleaned_data)

    def elbow_method(self):
        inertia = []
        for i in range(1,11):
            kmeans = KMeans(
                n_clusters=i, init="k-means++",
                n_init=10,
                tol=1e-04, random_state=42
            )
            kmeans.fit(self.scaled_data)
            inertia.append(kmeans.inertia_)
        fig = go.Figure(data=go.Scatter(x=np.arange(1,11),y=inertia))
        fig.update_layout(title="Inertia vs Cluster Number",xaxis=dict(range=[0,11],title="Cluster Number"),
                        yaxis={'title':'Inertia'},
                        annotations=[
                dict(
                    x=3,
                    y=inertia[2],
                    xref="x",
                    yref="y",
                    text="Elbow!",
                    showarrow=True,
                    arrowhead=7,
                    ax=20,
                    ay=-40
                )
            ])
        fig.show()

    def clustering(self):
        kmeans = KMeans(n_clusters=self.optimal_K)
        kmeans.fit(self.scaled_data)
        clusters=pd.DataFrame(self.cleaned_data,columns=self.df.drop(["trackId","recordingId"],axis=1).columns)
        clusters['label']=kmeans.labels_
        return clusters
    def polar_ploting(self):
        polar=self.clusters.groupby("label").mean().reset_index()
        polar=pd.melt(polar,id_vars=["label"])
        fig = px.line_polar(polar, r="value", theta="variable", color="label", line_close=True,height=800,width=1400)
        fig.show()

    def pi_ploting(self):
        pie=self.clusters.groupby('label').size().reset_index()
        pie.columns=['label','value']
        px.pie(pie,values='value',names='label',color=['blue','red','green']).show()


    def saving_data(self):
        self.clusters.insert(0, 'trackId', self.df['trackId'])
        self.clusters.insert(1, 'recordingId', self.df['recordingId'])
        self.clusters[self.clusters["label"]==0].to_csv("resultForLabel0.csv")
        self.clusters[self.clusters["label"]==1].to_csv("resultForLabel1.csv")
        self.clusters[self.clusters["label"]==2].to_csv("resultForLabel2.csv")
        self.clusters.to_csv("dataFrameWithPredictions.csv")