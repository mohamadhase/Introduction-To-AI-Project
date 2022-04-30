# 1- inD Dataset Volatility Measures Calculation
All the mentioned code and data in the "README.md" file can be found in the "Development" branch. Each team member's contribution to the code can also be found in the commits merged to the "Development" branch. The main will be used/merged to when reaching the final submission of this project.
## 1- Reading Data & Combining Files
- The "Data" class handles the combination of data and converting it to a dataframe (for the purpose of calculating the Volatilaty Measures). Using the join functionality we take all the files named "_tracks.csv" and place them onto a list using the glob method. Then we read each element in that list as a csv and convert it to a dataframe using the dataframe concat and map methods (The "tracksMeta" fiiles follow the same concept).
```ruby
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
```
- The "featureEngineering" class contains a the "dataFrameInitialize" method which takes the original dataframe and uses the "trackId" and "recordingId" from the "tracksMeta.csv" files as keys.
```ruby
def data_frame_init(self):
self.volatility_df["trackId"] = self.data.metas_df["trackId"]
self.volatility_df["recordingId"] = self.data.metas_df["recordingId"]
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
- Using the row passed through the "apply" method we compared the "TrackId" and the "recordingId" of the "result" dataframe, which only contains unique drivers, and original dataframe, which contains every frame recorded for each driver. Then took the needed column to calculate the mean/average of that column to then calculate the coefficients using the standard deviation for the respective column (Standard Deviation from the previously calculated Volatility Measure was not used because all the functions run in parallel to speed up the calculation process) and the given volatility measure formula.
```ruby
def calculate_speed_variation(self, row):
track_id = int(row["trackId"])
recording_id = int(row['recordingId'])
condition = (self.data.tracks_df["trackId"] == track_id) & (self.data.tracks_df["recordingId"] == recording_id)
ff = (self.data.tracks_df[condition]["xVelocity"])
dv1 = ff.std()
mean = self.data.tracks_df[condition]["xVelocity"].mean()
if(mean == 0):
return 0
return 100*(dv1/mean)
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
if Q1 + Q3 == 0 or math.isnan(Q1) or math.isnan(Q3):
return 0
result =  100*((Q3-Q1)/(Q3+Q1))
return result
```
### Percentage of Time Mean Exceeds Mean Plus Two Standard Deviations (Speed, Acceleration, Deceleration)
- Using the row passed through the "apply" method we compared the "TrackId" and the "recordingId" of the "result" dataframe, which only contains unique drivers, and original dataframe, which contains every frame recorded for each driver. Then calculated the mean for the retrieved values and the count of times that column exceeded the calculated mean plus two standard deviation (The standard deviation is the one previously-calculated for the matching column). Finally, we returned the result using the formula given in the Volatility Measure paper.
```ruby
def calculate_percentage_time_speed(self, row):
track_id = int(row["trackId"])
recording_id = int(row['recordingId'])
condition = (self.data.tracks_df["trackId"] == track_id) & (self.data.tracks_df["recordingId"] == recording_id)
ff = (self.data.tracks_df[condition]["xVelocity"])
dv1 = ff.std()
double_velocity_std = 2*dv1
filtered_df = (self.data.tracks_df[condition])
mean = filtered_df["xVelocity"].mean()
size_of_filtered_df = (filtered_df["xVelocity"]).shape[0]
number_of_speeds_exceeds_mean = (filtered_df[filtered_df["xVelocity"] >= (mean + double_velocity_std)]).shape[0]
return (100*(number_of_speeds_exceeds_mean/size_of_filtered_df))
```
### Applying Calculated Measures to The Dataframe
- The "apply" method uses the predefined "apply" functionality from the Pandas library to iterate through each row of the dataframe and applying the above mentioned method to every row. The resulting dataframe contains "recordingId", "trackId" (As keys) as well as all the calculated (13) Volatility Measures.
```ruby
def apply_dv1(self):
self.volatility_df["DV1"] = self.volatility_df.apply(self.calculate_speed_deviation, axis = 1)
```
- Finally, all the "apply" methods for the Volatility Measures are called in the "dv_application" method that runs each needed Measures in a thread, which allows all of them to run in parallel.
```ruby
def dv_application(self):
threads = [
Thread(target = self.apply_dv1),
Thread(target = self.apply_dv2),
Thread(target = self.apply_dv3),
Thread(target = self.apply_dv4),
Thread(target = self.apply_dv5),
Thread(target = self.apply_dv6),
Thread(target = self.apply_dv7),
Thread(target = self.apply_dv8),
Thread(target = self.apply_dv9),
Thread(target = self.apply_dv10),
Thread(target = self.apply_dv11),
Thread(target = self.apply_dv12),
Thread(target = self.apply_dv13)
]
for thread in threads:
thread.start()
for thread in threads:
thread.join()
```
# Part 2: Dataset Clean Up & Clustering
## 1- Data Exploration & EDA
## 2- Finding The Optimal Amount of Clusters Using The Elbow Method
- To be able to detect and find the optimal number of clusters, we have to run the K-Means Clustering algorithm with a random amount of clusters (1 to 10 in our case) to find the sum of squared distances to their closest cluster center for each cluster number's run and save that result to a list called "inertia". Then, using a plot, we represented the inertia of each run in comparison to its cluster number's run. Finally, we used the "KneeLocator" package to observe where the graph begings to flatten out so we could find the elbow point.
```ruby
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
```
- The plot shows that the optimal number of clusters is 5, but we ended up using the 3 for the number of clusters (because we're interested only in 3 classifications to the drivers which are conservative, normal, and aggressive)
## 3- Model Tranining & Result Extraction
## 4- Result Analysis
