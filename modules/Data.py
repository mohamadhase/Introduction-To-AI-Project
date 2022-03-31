import glob
import os.path
import pandas as pd
import math

class Data:
    def __init__(self):
        self.tracks = os.path.join("data/", "*_tracks.csv")
        print("hi1")
        self.tracks = glob.glob(self.tracks)
        print("hi2")

        self.tracks_df = pd.concat(map(pd.read_csv, self.tracks), ignore_index=True)  
        print("hi3")

        self.grouped_tracks_df = pd.DataFrame()
        print("hi4")

        self.avg_velocities = []
        print("h5")

        self.avg_accelerations = []
        print("hi6")
        self.calculateMean()
        print("hi7")
        self.velocitiesMean()
        print("hi8")
        self.accelerationsMean()
        print("hi9")
        
        
    def calculateMean(self):
        # calculates the means for all the columns based on the track id (driver)
        self.grouped_tracks_df = self.tracks_df.groupby(["trackId"]).mean()

    def velocitiesMean(self):
    # places the mean values for each track id (driver) into a list, to use as the mean for the velocities
        for avg_velocity in self.grouped_tracks_df["xVelocity"]:
            self.avg_velocities.append(avg_velocity)
        
    def accelerationsMean(self):
    # places the mean values for each track id (driver) into a list, to use as the mean for the accelerations
        for avg_acceleration in self.grouped_tracks_df["xAcceleration"]:
            self.avg_accelerations.append(avg_acceleration)









