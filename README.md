# inD Dataset Volatilaity Measures Calculation
All the mentioned code and data in the "README.md" file can be found in the "Development" branch. Each team member's contribution to the code can also be found in the commits merged to the "Development" branch. The main will be used/merged to when reaching the final submission of this project.
## 1- Reading Data & Combining Files
- The "Data" class handles the combination of data and converting it to a dataframe (for the purpose of calculating the Volatilaty Measures). Using the join functionality we take all the files named "_tracks.csv" and place them onto a list using the glob method. Then we read each element in that list as a csv and convert it to a dataframe using the dataframe concat and map methods (The "tracksMeta" fiiles follow the same concept).
```ruby
self.tracks = os.path.join("data/", "*_tracks.csv")
self.metas = os.path.join("data/", "*_tracksMeta.csv")
self.tracks = glob.glob(self.tracks)
self.metas = glob.glob(self.metas)
self.tracks_df = pd.concat(map(pd.read_csv, self.tracks), ignore_index=True)
self.metas_df = pd.concat(map(pd.read_csv, self.metas), ignore_index=True)
```
- The "featureEngineering" class contains a the "dataFrameInitialize" method which takes the original dataframe and uses the "trackId" and "recordingId" from the "tracksMeta.csv" files as keys.
```ruby
def dataFrameInitlize(self):
self.result["trackId"] = self.data.metas_df["trackId"]
self.result["recordingId"] = self.data.metas_df["recordingId"]
```
## 2- Feature Engineering
### Standard Deviation (Speed, Acceleration/Deceleration)
- Using the row passed through the "apply" method we compared the "TrackId" and the "recordingId" of the "result" dataframe, which only contains unique drivers, and original dataframe, which contains every frame recorded for each driver. Then took the required column for the matching volatility measure. Calculation for Acceleration/Deceleration follows the same concept.
```ruby
def calculate_speed_deviation(self,row):
track_id = int(row['trackId'])
recording_id = int(row['recordingId'])
condition = (self.data.tracks_df["trackId"] == track_id) & (self.data.tracks_df["recordingId"] == recording_id)
filtered_df = (self.data.tracks_df[condition]["xVelocity"])
sd = filtered_df.std()
return sd
```
### Coefficient of Variation (Speed, Acceleration, Deceleration)
- Using the row passed through the "apply" method we compared the "TrackId" and the "recordingId" of the "result" dataframe, which only contains unique drivers, and original dataframe, which contains every frame recorded for each driver. Then took the needed column to calculate the mean/average of that column to then calculate the coefficients using the previously-calculated standard deviation and the given volatility measure formula.
```ruby
def calculate_speed_variation(self,row):
track_id = int(row["trackId"])
recording_id = int(row["recordingId"])
DV1 = row["DV1"]
condition = (self.data.tracks_df["trackId"]==track_id) & (self.data.tracks_df["recordingId"]==recording_id)
mean = self.data.tracks_df[condition]["xVelocity"].mean()
return 100*(DV1/mean)
```
### Mean Absolute Deviation (Speed, Acceleration)
- Using the row passed through the "apply" method we compared the "TrackId" and the "recordingId" of the "result" dataframe, which only contains unique drivers, and original dataframe, which contains every frame recorded for each driver. Then took the required column for each given Volatility Measure forumla. Finally, using the "mad" predefined method from Pandas, we calculated the absolute value for each row.
```ruby
def calculate_abs_speed_deviation(self,row):
track_id = int(row["trackId"])
recording_id = int(row["recordingId"])
condition = (self.data.tracks_df["trackId"]==track_id) & (self.data.tracks_df["recordingId"]==recording_id)
calculated_df = (self.data.tracks_df[condition]["xVelocity"])
return calculated_df.mad()
```
### Quantile Coefficient of Variation (Normalised Speed, Acceleration, Deceleration)
- Using the row passed through the "apply" method we compared the "TrackId" and the "recordingId" of the "result" dataframe, which only contains unique drivers, and original dataframe, which contains every frame recorded for each driver. Then, using the "quantile" predefined functionality, we passed the percentile needed (25th & 75th), then checked if any calculated value equals 0 to avoid inputting "Not a Number (NaN)" values into the dataframe. Finally, we returned the result based on the given formula from the Volatility Measures paper.
```ruby
def calculate_quantile_co_speed(self,row):
track_id = int(row["trackId"])
recording_id = int(row["recordingId"])
condition = (self.data.tracks_df["trackId"]==track_id) & (self.data.tracks_df["recordingId"]==recording_id)
Q1 = ((self.data.tracks_df[condition]["xVelocity"]).quantile(0.25))
Q3 = ((self.data.tracks_df[condition]["xVelocity"]).quantile(0.75))
if((Q3+Q1 )== 0):
return 0
result =  100*((Q3-Q1)/(Q3+Q1))
return result
```
### Percentage of Time Exceeding Mean Plus Two Standard Deviations (Speed, Acceleration, Deceleration)
- Using the row passed through the "apply" method we compared the "TrackId" and the "recordingId" of the "result" dataframe, which only contains unique drivers, and original dataframe, which contains every frame recorded for each driver. Then calculated the mean for the retrieved values and the count of times that column exceeded the calculated mean plus two standard deviation (The standard deviation is the one previously-calculated for the matching column). Finally, we returned the result using the formula given in the Volatility Measure paper.
```ruby
def calculate_percentage_time_speed(self,row):
track_id = int(row["trackId"])
recording_id = int(row["recordingId"])
sd_of_V = row["DV1"]
condition = (self.data.tracks_df["trackId"]==track_id) & (self.data.tracks_df["recordingId"]==recording_id)
calculated_df = (self.data.tracks_df[condition]["xVelocity"])
mean = calculated_df.mean()
size_of_calculated_df = calculated_df.count()
number_of_speeds_exceeds_mean = calculated_df[calculated_df["xVelocity"] >= mean + (2*sd_of_V)].count()
return 100*(number_of_speeds_exceeds_mean/size_of_calculated_df)
```
### Applying Calculated Measures to The Dataframe
- The "apply" method uses the predefined "apply" functionality from the Pandas library to iterate through each row of the dataframe and applying the above mentioned method to every row. The resulting dataframe contains "recordingId", "trackId" (As keys) as well as all the calculated (13) Volatility Measures.
```ruby
def apply_dv1(self):
self.result["DV1"] = self.result.apply(self.calculate_speed_deviation, axis=1)
```
