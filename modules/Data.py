import glob
import os.path
import pandas as pd
import time

class Data:
    def __init__(self):
        start_time = time.perf_counter ()
        self.tracks = self.get_tracks_paths()
        end_time = time.perf_counter ()
        print(end_time - start_time, "seconds  for getTracksPaths")


        start_time = time.perf_counter ()
        self.metas = self.get_tracks_meta_paths()
        end_time = time.perf_counter ()
        print(end_time - start_time, "seconds  for getmetasPaths")





        self.tracks = glob.glob(self.tracks)
        self.metas = glob.glob(self.metas)

        start_time = time.perf_counter ()
        self.tracks_df = self.init_tracks_df()
        end_time = time.perf_counter ()
        print(end_time - start_time, "seconds  for InitTracksDF")

        start_time = time.perf_counter ()
        self.metas_df = self.init_tracks_meta_df()
        end_time = time.perf_counter ()
        print(end_time - start_time, "seconds  for InitTracksMetaDf")



    def get_tracks_paths(self):
        return os.path.join("data/", "*_tracks.csv")

    def get_tracks_meta_paths(self):
        return os.path.join("data/", "*_tracksMeta.csv")

    def init_tracks_df(self):
        return pd.concat(map(pd.read_csv, self.tracks), ignore_index = True)

    def init_tracks_meta_df(self):
        return pd.concat(map(pd.read_csv, self.metas), ignore_index = True)
