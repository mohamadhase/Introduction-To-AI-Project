import glob
import os.path
import pandas as pd
import math
from modules.Data import Data
class FeatureEngineering:
    def __init__(self,data:Data):
        self.data = data

# Ahmad
    def calculate_speed_deviation(self,row):
        track_id = int(row['trackId'])
        velocity = row['xVelocity']
        return math.sqrt(math.pow((velocity - self.data.avg_velocities[track_id]), 2) / len(self.data.tracks_df.index))


    # Ahmad
    def calculate_long_a_deviation(self,row):
        track_id = int(row["trackId"])
        long_a = row["xAcceleration"]
        return math.sqrt(math.pow(long_a - self.data.avg_accelerations[track_id], 2) / len(self.data.tracks_df.index))


    # Nasser
    def calculate_speed_variation(self,row):
        track_id = int(row["trackId"])
        print("hi")


    # Ahmad
    def calculate_acceleration_variation(self,row):  # Use only the positive values from xAcceleration
        track_id = int(row["trackId"])


    # Omar
    def calculate_deceleration_variation(self,row):  # Use only the negative values from xAcceleration
        track_id = int(row["trackId"])


    # Karam
    def calculate_abs_speed_deviation(self,row):
        track_id = int(row["trackId"])


    # Yaseen
    def calculate_abs_acceleration_deviation(self,row):  # Use only positive values from xAcceleration
        track_id = int(row["trackId"])


    # Nasser
    def calculate_quantile_co_speed(self,row):
        track_id = int(row["trackId"])


    # Omar
    def calculate_quantile_co_acceleration(self,row):  # Use only the positive values for xAcceleration
        track_id = int(row["trackId"])


    # Hmouda
    def calculate_quantile_co_deceleration(self,row):  # Use only the negative values for xAcceleration
        track_id = int(row["trackId"])


    # Karam
    def calculate_percentage_time_speed(self,row):
        track_id = int(row["trackId"])


    # Yaseen
    def calculate_percentage_time_acceleration(self,row):  # Use only the positive values for xAcceleration
        track_id = int(row["trackId"])


    # Hmouda
    def calculate_percentage_time_deceleration(self,row):  # Use only the negative values for xAcceleration
        track_id = int(row["trackId"])


    def apply_dv1(self):
        self.data.tracks_df["DV1"] = self.data.tracks_df.apply(self.calculate_speed_deviation, axis=1)


    def apply_dv2(self):
        self.data.tracks_df["DV2"] = self.data.tracks_df.apply(self.calculate_long_a_deviation, axis=1)


    def apply_dv3(self):
        self.data.tracks_df["DV3"] = self.data.tracks_df.apply(self.calculate_speed_variation, axis=1)


    def apply_dv4(self):
        self.data.tracks_df["DV4"] = self.data.tracks_df.apply(self.calculate_acceleration_variation, axis=1)


    def apply_dv5(self):
        self.data.tracks_df["DV5"] = self.data.tracks_df.apply(self.calculate_deceleration_variation, axis=1)


    def apply_dv6(self):
        self.data.tracks_df["DV6"] = self.data.tracks_df.apply(self.calculate_abs_speed_deviation, axis=1)


    def apply_dv7(self):
        self.data.tracks_df["DV7"] = self.data.tracks_df.apply(self.calculate_abs_acceleration_deviation, axis=1)


    def apply_dv8(self):
        self.data.tracks_df["DV8"] = self.data.tracks_df.apply(self.calculate_quantile_co_speed, axis=1)


    def apply_dv9(self):
        self.data.tracks_df["DV9"] = self.data.tracks_df.apply(self.calculate_quantile_co_acceleration, axis=1)


    def apply_dv10(self):
        self.data.tracks_df["DV10"] = self.data.tracks_df.apply(self.calculate_quantile_co_deceleration, axis=1)


    def apply_dv11(self):
        self.data.tracks_df["DV11"] = self.data.tracks_df.apply(self.calculate_percentage_time_speed, axis=1)


    def apply_dv12(self):
        self.data.tracks_df["DV12"] = self.data.tracks_df.apply(self.calculate_percentage_time_acceleration, axis=1)


    def apply_dv13(self):
        self.data.tracks_df["DV13"] =  self.data.tracks_d.apply(self.calculate_percentage_time_deceleration, axis=1)


