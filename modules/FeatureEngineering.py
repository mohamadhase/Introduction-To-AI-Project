import pandas as pd
from modules.Data import Data
import math
class FeatureEngineering:
    def __init__(self, data:Data):
        self.data = data
        self.volatility_df = pd.DataFrame()
        self.data_frame_init()
        self.dv_application()

        
    def data_frame_init(self):
      self.volatility_df["trackId"] = self.data.metas_df["trackId"]
      self.volatility_df["recordingId"] = self.data.metas_df["recordingId"]

    def dv_application(self):
        self.apply_dv1()
        self.apply_dv2()
        self.apply_dv3()
        self.apply_dv4()
        self.apply_dv5()
        self.apply_dv6()
        self.apply_dv7()
        self.apply_dv8()
        self.apply_dv9()
        self.apply_dv10()
        self.apply_dv11()
        self.apply_dv12()
        self.apply_dv13()
        print("process Done")
        self.save_to_csv()



    def save_to_csv(self):
        self.volatility_df.to_csv("volatility_df.csv")

        
   # Ahmad
    def calculate_speed_deviation(self, row):
        track_id = int(row['trackId'])
        recording_id = int(row['recordingId'])
        condition = (self.data.tracks_df["trackId"] == track_id) & (self.data.tracks_df["recordingId"] == recording_id)
        filtered_df = (self.data.tracks_df[condition]["xVelocity"])
        std = filtered_df.std()
        return std



   # Ahmad
    def calculate_long_a_deviation(self, row):
        track_id = int(row["trackId"])
        recording_id = int(row['recordingId'])
        condition = (self.data.tracks_df["trackId"] == track_id) & (self.data.tracks_df["recordingId"] == recording_id)
        filtered_df = (self.data.tracks_df[condition]["lonAcceleration"])
        std = filtered_df.std()
        return std


    # Nasser
    def calculate_speed_variation(self, row):
        track_id = int(row["trackId"])
        recording_id = int(row['recordingId'])
        dv1 = row["DV1"]
        condition = (self.data.tracks_df["trackId"] == track_id) & (self.data.tracks_df["recordingId"] == recording_id)
        mean = self.data.tracks_df[condition]["xVelocity"].mean()
        if(mean == 0):
            return 0
        return 100*(dv1/mean)


    # Ahmad
    def calculate_acceleration_variation(self, row):  # Use only the positive values from xAcceleration
        track_id = int(row["trackId"])
        recording_id = int(row['recordingId'])
        condition = (self.data.tracks_df["trackId"] == track_id) & (self.data.tracks_df["recordingId"] == recording_id)
        filtered_df = (self.data.tracks_df[condition])
        filtered_df_acc = (filtered_df[filtered_df["lonAcceleration"] >= 0]["lonAcceleration"])
        std_acc = filtered_df_acc.std()
        mean = filtered_df_acc.mean()

        if mean == 0 or math.isnan(mean):
            return 0
        

        return 100 * (std_acc / mean)


    # Omar
    def calculate_deceleration_variation(self, row):  # Use only the negative values from lonAcceleration
        track_id = int(row["trackId"])
        recording_id = int(row['recordingId'])
        condition = (self.data.tracks_df["trackId"] == track_id) & (self.data.tracks_df["recordingId"] == recording_id)
        filtered_df = (self.data.tracks_df[condition])
        deceleration_df = (filtered_df[filtered_df["lonAcceleration"] < 0]["lonAcceleration"])
        std_dec = deceleration_df.std()
        mean = deceleration_df.mean()
        if mean == 0 or math.isnan(mean):
            return 0

        return 100 * (std_dec / mean) 


    # Karam
    def calculate_abs_speed_deviation(self, row):
        track_id = int(row["trackId"])
        recording_id = int(row['recordingId'])
        condition = (self.data.tracks_df["trackId"] == track_id) & (self.data.tracks_df["recordingId"] == recording_id)
        filtered_df = (self.data.tracks_df[condition])
        velocity_df = filtered_df["xVelocity"]
        return velocity_df.mad()

    # Yaseen
    def calculate_abs_acceleration_deviation(self, row):  # Use only positive values from lonAcceleration
        track_id = int(row["trackId"])
        recording_id = int(row['recordingId'])
        condition = (self.data.tracks_df["trackId"] == track_id) & (self.data.tracks_df["recordingId"] == recording_id)
        filtered_df = self.data.tracks_df[condition]
        acceleration_df = filtered_df[filtered_df["lonAcceleration"] >= 0] 
        acc_mad = acceleration_df["lonAcceleration"].mad()
        
        return acc_mad


    # Nasser
    def calculate_quantile_co_speed(self, row):
        track_id = int(row["trackId"])
        recording_id = int(row['recordingId'])
        condition = (self.data.tracks_df["trackId"] == track_id) & (self.data.tracks_df["recordingId"] == recording_id)
        filtered_df = self.data.tracks_df[condition]["xVelocity"]
        Q1 = (filtered_df).quantile(0.25)
        Q3 = (filtered_df).quantile(0.75)
        if Q1 + Q3 == 0 or math.isnan(Q1) or math.isnan(Q3) :
            return 0
        result =  100*((Q3-Q1)/(Q3+Q1))
        return result


    # Omar
    def calculate_quantile_co_acceleration(self, row):  # Use only the positive values for lonAcceleration
        track_id = int(row["trackId"])
        recording_id = int(row['recordingId'])
        condition = (self.data.tracks_df["trackId"] == track_id) & (self.data.tracks_df["recordingId"] == recording_id)

        filtered_df = self.data.tracks_df[condition]
        acceleration_df = filtered_df[filtered_df["lonAcceleration"] >= 0]["lonAcceleration"]
        Q1 = acceleration_df.quantile(0.25)
        Q3 = acceleration_df.quantile(0.75)
        if Q1 + Q3 == 0 or math.isnan(Q1) or math.isnan(Q3) :
            return 0
        return 100*((Q3-Q1)/(Q3+Q1))
        



    # Hmouda
    def calculate_quantile_co_deceleration(self, row):  # Use only the negative values for lonAcceleration
        track_id = int(row["trackId"])
        recording_id = int(row['recordingId'])
        condition = (self.data.tracks_df["trackId"] == track_id) & (self.data.tracks_df["recordingId"] == recording_id)

        filtered_df = self.data.tracks_df[condition]

        decleration_df = filtered_df[filtered_df["lonAcceleration"] < 0]["lonAcceleration"]
        Q1 = decleration_df.quantile(0.25)
        Q3 = decleration_df.quantile(0.75)
        if Q1 + Q3 == 0 or math.isnan(Q1) or math.isnan(Q3) :
            return 0
        return 100 * ((Q3 - Q1) / (Q3 + Q1))


    # Karam
    def calculate_percentage_time_speed(self, row):
        track_id = int(row["trackId"])
        recording_id = int(row['recordingId'])
        condition = (self.data.tracks_df["trackId"] == track_id) & (self.data.tracks_df["recordingId"] == recording_id)
        double_velocity_std = 2*row["DV1"]
        filtered_df = (self.data.tracks_df[condition])
        mean = filtered_df["xVelocity"].mean()
        size_of_filtered_df = (filtered_df["xVelocity"]).shape[0]
        number_of_speeds_exceeds_mean = (filtered_df[filtered_df["xVelocity"] >= (mean + double_velocity_std)]).shape[0]
        return (100*(number_of_speeds_exceeds_mean/size_of_filtered_df))


    # Yaseen
    def calculate_percentage_time_acceleration(self, row):  # Use only the positive values for lonAcceleration
        track_id = int(row["trackId"])
        recording_id = int(row['recordingId'])
        condition = (self.data.tracks_df["trackId"] == track_id) & (self.data.tracks_df["recordingId"] == recording_id)
        filtered_df = self.data.tracks_df[condition]
        acc_df = filtered_df[filtered_df["lonAcceleration"] >= 0] 
        mean = acc_df["lonAcceleration"].mean()
        double_acc_std = acc_df["lonAcceleration"].std()
        volatility_df = (acc_df[acc_df["lonAcceleration"] >= (mean + double_acc_std)]).shape[0]
        if(not acc_df.shape[0]):
            return 0
        return 100*(volatility_df/acc_df.shape[0])


    # Hmouda
    def calculate_percentage_time_deceleration(self, row):  # Use only the negative values for xAcceleration
        track_id = int(row["trackId"])
        recording_id = int(row['recordingId'])
        condition = (self.data.tracks_df["trackId"] == track_id) & (self.data.tracks_df["recordingId"] == recording_id)
        filtered_df = self.data.tracks_df[condition]
        dec_df = filtered_df[filtered_df["lonAcceleration"] < 0] 
        mean = dec_df["lonAcceleration"].mean()
        double_dec_std = dec_df["lonAcceleration"].std()
        volatility_df = (dec_df[dec_df["lonAcceleration"] >= (mean + double_dec_std)]).shape[0]
        if(not dec_df.shape[0]):
            return 0
        return 100*(volatility_df/dec_df.shape[0])
        

    def apply_dv1(self):
        self.volatility_df["DV1"] = self.volatility_df.apply(self.calculate_speed_deviation, axis = 1)



    def apply_dv2(self):
        self.volatility_df["DV2"] = self.volatility_df.apply(self.calculate_long_a_deviation, axis = 1)



    def apply_dv3(self):
        self.volatility_df["DV3"] = self.volatility_df.apply(self.calculate_speed_variation, axis = 1)


    def apply_dv4(self):
        self.volatility_df["DV4"] = self.volatility_df.apply(self.calculate_acceleration_variation, axis = 1)



    def apply_dv5(self):
        self.volatility_df["DV5"] = self.volatility_df.apply(self.calculate_deceleration_variation, axis = 1)


    def apply_dv6(self):
        self.volatility_df["DV6"] = self.volatility_df.apply(self.calculate_abs_speed_deviation, axis = 1)


    def apply_dv7(self):
        self.volatility_df["DV7"] = self.volatility_df.apply(self.calculate_abs_acceleration_deviation, axis = 1)


    def apply_dv8(self):
        self.volatility_df["DV8"] = self.volatility_df.apply(self.calculate_quantile_co_speed, axis = 1)


    def apply_dv9(self):
        self.volatility_df["DV9"] = self.volatility_df.apply(self.calculate_quantile_co_acceleration, axis = 1)


    def apply_dv10(self):
        self.volatility_df["DV10"] = self.volatility_df.apply(self.calculate_quantile_co_deceleration, axis = 1)


    def apply_dv11(self):
        self.volatility_df["DV11"] = self.volatility_df.apply(self.calculate_percentage_time_speed, axis = 1)


    def apply_dv12(self):
        self.volatility_df["DV12"] = self.volatility_df.apply(self.calculate_percentage_time_acceleration, axis = 1)


    def apply_dv13(self):
        self.volatility_df["DV13"] =  self.volatility_df.apply(self.calculate_percentage_time_deceleration, axis = 1)


