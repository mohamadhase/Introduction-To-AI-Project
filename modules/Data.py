import glob
import os.path
import pandas as pd


class Data:
    def __init__(self):
        self.tracks = self.get_tracks_paths()
        self.metas = self.get_tracks_meta_paths()
        self.tracks = glob.glob(self.tracks)
        self.metas = glob.glob(self.metas)
        self.tracks_df = self.init_tracks_df()
        self.metas_df = self.init_tracks_meta_df()

    def get_tracks_paths(self):
        return os.path.join("data/", "*_tracks.csv")

    def get_tracks_meta_paths(self):
        return os.path.join("data/", "*_tracksMeta.csv")

    def init_tracks_df(self):
        return pd.concat(map(pd.read_csv, self.tracks), ignore_index = True)

    def init_tracks_meta_df(self):
        return pd.concat(map(pd.read_csv, self.metas), ignore_index = True)
