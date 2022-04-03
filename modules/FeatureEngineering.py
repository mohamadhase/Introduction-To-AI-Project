import pandas as pd
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
    def calculate_acceleration_variation(self,row):  # Use only the positive values from lonAcceleration
        track_id = int(row["trackId"])
        filtered_df = (self.data.tracks_df[self.data.tracks_df["trackId"] == track_id])
        filtered_df_acc = (filtered_df[filtered_df["lonAcceleration"] > 0]["lonAcceleration"])
        sd_dec = filtered_df_acc.std()
        mean = filtered_df_acc.mean()

        if mean == 0:
            return 0

        return 100 * (sd_dec / mean)


    # Omar
    def calculate_deceleration_variation(self,row):  # Use only the negative values from lonAcceleration
        track_id = int(row["trackId"])
        trackDF = (self.data.tracks_df[self.data.tracks_df["trackId"] == track_id])
        Deceleration = (trackDF[trackDF["lonAcceleration"] < 0]["lonAcceleration"])
        std = Deceleration.std()
        mean = Deceleration.mean()
        if mean == 0:
            return 0

        return 100 * (std / mean) 


    # Karam
    def calculate_abs_speed_deviation(self,row):
        track_id = int(row["trackId"])
        calculated_df = (self.data.tracks_df[self.data.tracks_df["trackId"] == track_id]["xVelocity"])
        return calculated_df.mad()

    # Yaseen
    def calculate_abs_acceleration_deviation(self,row):  # Use only positive values from lonAcceleration
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
    def calculate_quantile_co_acceleration(self,row):  # Use only the positive values for lonAcceleration
        track_id = int(row["trackId"])
        trackDF = self.data.tracks_df[self.data.tracks_df["trackId"]==track_id]
        Acceleration = trackDF[trackDF["lonAcceleration"]>=0]
        Q1 = Acceleration["lonAcceleration"].quantile(0.25)
        Q3 = Acceleration["lonAcceleration"].quantile(0.75)
        if Q1 + Q3 == 0 :
            return 0
        return 100*((Q3-Q1)/(Q3+Q1))
        



    # Hmouda
    def calculate_quantile_co_deceleration(self,row):  # Use only the negative values for lonAcceleration
        track_id = int(row["trackId"])
        trackDf = self.data.tracks_df[self.data.tracks_df["trackId"] == track_id]
        Decleration = trackDf[trackDf["lonAcceleration"] < 0]
        Q1 = Decleration["lonAcceleration"].quantile(0.25)
        Q3 = Decleration["lonAcceleration"].quantile(0.75)
        if Q1 + Q3 == 0 :
            return 0
        return 100 * ((Q3 - Q1) / (Q3 + Q1))


    # Karam
    def calculate_percentage_time_speed(self,row):
        track_id = int(row["trackId"])
        sd_of_V = row["DV1"]
        calculated_df = (self.data.tracks_df[self.data.tracks_df["trackId"]==track_id]["xVelocity"])
        mean = calculated_df.mean()
        size_of_calculated_df = calculated_df.count()
        number_of_speeds_exceeds_mean = calculated_df[calculated_df["xVelocity"] >= mean + (2*sd_of_V)].count()
        return 100*(number_of_speeds_exceeds_mean/size_of_calculated_df)


    # Yaseen
    def calculate_percentage_time_acceleration(self,row):  # Use only the positive values for lonAcceleration
        track_id = int(row["trackId"])


    # Hmouda
    def calculate_percentage_time_deceleration(self,row):  # Use only the negative values for xAcceleration
        track_id = int(row["trackId"])
        singleTrackData= self.data.tracks_df[self.data.tracks_df["trackId"]==track_id]
        SDtrack = singleTrackData["lonAcceleration"].std()
        MeanTrack = singleTrackData["lonAcceleration"].mean()
        lessThandf = singleTrackData[singleTrackData["lonAcceleration"]>=(MeanTrack+2*SDtrack)]
        lessThanCount = lessThandf["lonAcceleration"].shape[0]
        x =  100 * (lessThanCount/(singleTrackData.shape[0]))
        return x
        

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
        self.result["DV5"] = self.result.apply(self.calculate_deceleration_variation, axis=1)


    def apply_dv6(self):
        self.result["DV6"] = self.result.apply(self.calculate_abs_speed_deviation, axis=1)


    def apply_dv7(self):
        self.result["DV7"] = self.result.apply(self.calculate_abs_acceleration_deviation, axis=1)


    def apply_dv8(self):
        self.result["DV8"] = self.result.apply(self.calculate_quantile_co_speed, axis=1)
        print(self.result)


    def apply_dv9(self):
        self.result["DV9"] = self.result.apply(self.calculate_quantile_co_acceleration, axis=1)


    def apply_dv10(self):
        self.result["DV10"] = self.result.apply(self.calculate_quantile_co_deceleration, axis=1)


    def apply_dv11(self):
        self.result["DV11"] = self.result.apply(self.calculate_percentage_time_speed, axis=1)


    def apply_dv12(self):
        self.result["DV12"] = self.result.apply(self.calculate_percentage_time_acceleration, axis=1)


    def apply_dv13(self):
        self.result["DV13"] =  self.result.apply(self.calculate_percentage_time_deceleration, axis=1)


