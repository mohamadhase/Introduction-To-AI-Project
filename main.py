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

def main():
    # data = Data()

    # featureEngineering = FeatureEngineering(data)
    df = pd.read_csv("volatility_df.csv")
    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.dropna()
    df = df.reset_index()
    # fig = px.scatter_matrix(df.drop(["trackId","recordingId"],axis=1),
    # width=1200, height=1600)
    # fig.show()
    X = df.drop(["trackId","recordingId","index"],axis=1)

    scaler = MinMaxScaler()
    scaler.fit(X)
    X=scaler.transform(X)
    # inertia = []
    # for i in range(1,11):
    #     kmeans = KMeans(
    #         n_clusters=i, init="k-means++",
    #         n_init=10,
    #         tol=1e-04, random_state=42
    #     )
    #     kmeans.fit(X)
    #     inertia.append(kmeans.inertia_)
    # fig = go.Figure(data=go.Scatter(x=np.arange(1,11),y=inertia))
    # fig.update_layout(title="Inertia vs Cluster Number",xaxis=dict(range=[0,11],title="Cluster Number"),
    #                 yaxis={'title':'Inertia'},
    #                 annotations=[
    #         dict(
    #             x=3,
    #             y=inertia[2],
    #             xref="x",
    #             yref="y",
    #             text="Elbow!",
    #             showarrow=True,
    #             arrowhead=7,
    #             ax=20,
    #             ay=-40
    #         )
    #     ])
    # fig.show()
    kmeans = KMeans(
            n_clusters=3, init="k-means++",
            n_init=10,
            tol=1e-04, random_state=42
        )

    kmeans.fit(X)
    
    clusters=pd.DataFrame(X,columns=df.drop(["index","trackId","recordingId"],axis=1).columns)
    clusters['label']=kmeans.labels_
    polar=clusters.groupby("label").mean().reset_index()
    polar=pd.melt(polar,id_vars=["label"])

    fig4 = px.line_polar(polar, r="value", theta="variable", color="label", line_close=True,height=800,width=1400)
    fig4
    pie=clusters.groupby('label').size().reset_index()
    pie.columns=['label','value']
    px.pie(pie,values='value',names='label',color=['blue','red','green'])
    df["label"] = clusters["label"]
    print(df[df["label"]==0]["DV2"].sum())
    print(df[df["label"]==1]["DV2"].sum())

if __name__ == "__main__":
    main()


    #0 -> semms to be normal
    #1 ->seems to be aggr
    #2 -> for now its for cars stop at the right