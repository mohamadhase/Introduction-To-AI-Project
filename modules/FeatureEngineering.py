from cmath import nan
import glob
import os.path
from numpy import NaN
import pandas as pd
import math
from modules.Data import Data
class FeatureEngineering:
    def __init__(self,data:Data):
        self.data = data
        self.result = pd.DataFrame()
        self.dataFrameInitlize()

        
    def dataFrameInitlize(self):
       
      self.result["trackId"] = self.data.tracks_df["trackId"].unique()
        
   # Ahmad
    def calculate_speed_deviation(self,row):
        track_id = int(row['trackId'])
        filtered_df = (self.data.tracks_df[self.data.tracks_df["trackId"] == track_id]["xVelocity"])
        sd = filtered_df.std()
        return sd


   # Ahmad
    def calculate_long_a_deviation(self,row):
        track_id = int(row["trackId"])
        filtered_df = (self.data.tracks_df[self.data.tracks_df["trackId"] == track_id]["lonAcceleration"])
        sd = filtered_df.std()
        return sd


    # Nasser
    def calculate_speed_variation(self,row):
        track_id = int(row["trackId"])
        DV1 = row["DV1"]
        mean = self.data.tracks_df[self.data.tracks_df["trackId"]==track_id]["xVelocity"].mean()
        return 100*(DV1/mean)


    # Ahmad
    def calculate_acceleration_variation(self,row):  # Use only the positive values from xAcceleration
        track_id = int(row["trackId"])
        filtered_df = (self.data.tracks_df[self.data.tracks_df["trackId"] == track_id])
        filtered_df_acc = (filtered_df[filtered_df["lonAcceleration"] > 0]["lonAcceleration"])
        sd_dec = filtered_df_acc.std()
        mean = filtered_df_acc.mean()

        if mean == 0:
            return 0

        return 100 * (sd_dec / mean)


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
        
        Q1 = ((self.data.tracks_df[self.data.tracks_df["trackId"]==track_id]["xVelocity"]).quantile(0.25))
        Q3 = ((self.data.tracks_df[self.data.tracks_df["trackId"]==track_id]["xVelocity"]).quantile(0.75))
        if((Q3+Q1 )== 0):
            return 0
        result =  100*((Q3-Q1)/(Q3+Q1))
        return result


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
        dec1 = self.data.tracks_df[self.data.tracks_df["tracID"]==track_id]
        sd = row["DV2"]
        dec = dec1[dec1["xAcceleration"]<0]
        mean  =  dec["xAcceleration"].mean()
        count = dec[dec["xAcceleration"]>=mean+(2*sd)].count()
        return 100* (count/dec.count())
        

    def apply_dv1(self):
        self.result["DV1"] = self.result.apply(self.calculate_speed_deviation, axis=1)
        print(self.result)


    def apply_dv2(self):
        self.result["DV2"] = self.result.apply(self.calculate_long_a_deviation, axis=1)
        print(self.result)


    def apply_dv3(self):
        self.result["DV3"] = self.result.apply(self.calculate_speed_variation, axis=1)


    def apply_dv4(self):
        self.result["DV4"] = self.result.apply(self.calculate_acceleration_variation, axis=1)
        print(self.result)


    def apply_dv5(self):
        self.data.tracks_df["DV5"] = self.data.tracks_df.apply(self.calculate_deceleration_variation, axis=1)


    def apply_dv6(self):
        self.data.tracks_df["DV6"] = self.data.tracks_df.apply(self.calculate_abs_speed_deviation, axis=1)


    def apply_dv7(self):
        self.data.tracks_df["DV7"] = self.data.tracks_df.apply(self.calculate_abs_acceleration_deviation, axis=1)


    def apply_dv8(self):
         self.result["DV8"] = self.result.apply(self.calculate_quantile_co_speed, axis=1)
         print(self.result)


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


