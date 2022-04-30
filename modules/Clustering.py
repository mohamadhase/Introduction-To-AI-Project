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
            label0 = pd.read_csv("Label0.csv")
       label1 = pd.read_csv("Label1.csv")
    label2 = pd.read_csv("Label2.csv")
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set(title='An Axes Title', xlim=[0.5, 4.5], ylim=[-3, 7], ylabel='Y-Axis Label', xlabel='X-Axis Label')
    # meanLabel1 = label0["DV1"].mean()
    # meanLabel2 = label1["DV1"].mean()
    # print(meanLabel1)
    # print(meanLabel2)
    # plt.plot(meanLabel1, meanLabel2)
    # plt.show()
    plt.plot(label0["DV1"])
    plt.plot(label1["DV1"])
    plt.plot(label2["DV1"])
    plt.show()
    # print(label0["DV1"].mean())
    # print(label1["DV1"].mean())
    # print(label2["DV1"].mean())

    def scaling_data(self):
        scaler = MinMaxScaler()
        scaler.fit(self.cleaned_data)
        return scaler.transform(self.cleaned_data)

    def elbow_method(self):
        inertia = []
        k_range = range(1, 11)
        for k in k_range:
            kmeans_model = KMeans(n_clusters=k)
            kmeans_model.fit(X)
            inertia.append(kmeans_model.inertia_)

        plt.figure(figsize=(16, 8))
        plt.plot(k_range, inertia, 'bx-')
        plt.xlabel('Number of Clusters')
        plt.ylabel('Inertia')
        plt.xticks(k_range)
        x = range(1, len(inertia) + 1)
        kn = KneeLocator(x, inertia, curve='convex', direction='decreasing')
        plt.annotate("Elbow Point", va='center', ha='right', xy=(kn.knee, inertia[kn.knee - 1]),
                     xytext=(kn.knee + 0.5, inertia[4] + 200),
                     arrowprops={'arrowstyle': '-|>', 'lw': 1, 'color': 'black'})
        plt.annotate("Chosen K", va='center', ha='right', xy=(3, inertia[2]),
                     xytext=(3.5, inertia[2] + 200),
                     arrowprops={'arrowstyle': '-|>', 'lw': 1, 'color': 'black'})
        plt.title('Elbow Method Showing The Optimal K')
        plt.show()

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
