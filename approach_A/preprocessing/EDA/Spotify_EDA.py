import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

df_musical_features = pd.read_csv(musical_features_path, sep=' ')
df_musical_features.rename(columns={'uri':'track_uri'}, inplace=True)
df_playlist_features = pd.read_csv(playlist_path, sep=' ')


# column names and shapes
print(f'column_names of musical_features: {df_musical_features.columns}')
print(f'column_names of playlist_features: {df_playlist_features.columns}')

print(f'shape of musical_features: {df_musical_features.shape}')
print(f'shape of playlist_features: {df_playlist_features.shape}')

columns = ['track_uri', 'track_name', 'artist_name']
req_col_df = df_playlist_features[columns]
df = pd.merge(req_col_df, df_musical_features, how='inner', on='track_uri')
print(df.head())

musical_columns = ['popularity', 'acousticness', 'danceability', 'duration_ms', 
                           'energy', 'instrumentalness', 'key', 'liveness', 'loudness', 'mode', 'speechiness', 'tempo', 'valence', 'year']
print(df[musical_columns].head())
print(df_musical_features.info())
print(df_musical_features.describe())

# df_musical_features = df_musical_features.sample(n=10000)
sc_plot1 = sns.pairplot(df_musical_features[['popularity', 'acousticness', 'danceability', 'duration_ms', 
                           'energy', 'instrumentalness']], diag_kind='kde')

df_musical_features = df_musical_features.sample(n=10000)
sc_plot1 = sns.pairplot(df_musical_features[['popularity', 'acousticness', 'danceability', 'duration_ms', 
                           'energy', 'instrumentalness']], diag_kind='kde')

'estimate correlations in matrix form with annotation bar'
numeric=['popularity', 'acousticness', 'danceability', 
        'duration_ms', 'energy', 'instrumentalness', 
        'liveness', 'loudness', 'speechiness', 'tempo', 'valence', 'mode', 'key']

corr_matrix = df_musical_features[numeric].corr()
mask = np.zeros_like(corr_matrix)
traingle_indices = np.triu_indices_from(corr_matrix)
mask[traingle_indices] = True
y, x = plt.subplots(figsize=(9, 7))

heatmap = sns.heatmap(corr_matrix, mask=mask, annot=True, annot_kws={'size':10},  fmt=".2f", linewidths=.5 )
plt.show()

# plot for energy-loudness pair 
sns.jointplot(x="loudness", y="energy", data=df_musical_features, kind="hex", height=4.5)

plt.annotate('Energy-loudness relation',
            xy=[0.1, 0.6],
            xytext=[1, 1.2],
            fontsize=14,
            arrowprops=dict(color='grey',
                            arrowstyle='simple',
                            shrinkA=4,
                            shrinkB=4))

# plot for energy-acousticness pair 
sns.jointplot(x="acousticness", y="energy", data=df_musical_features, kind="hex", height=4.5)


plt.annotate('Energy-acousticness relation',
            xy=[0.1, 0.6],
            xytext=[1, 1.2],
            fontsize=14,
            arrowprops=dict(color='grey',
                            arrowstyle='simple',
                            shrinkA=4,
                            shrinkB=4))

def plot_grid(col_name, i, len):
'''Plot a grid of images correaponding to distribution of different musical features in the dataset.
'''
  tempo_np = df_musical_features[col_name]
  ax5 = fig5.add_subplot(5,3,i)
  ax5.set_xlabel(f'{col_name.capitalize()}')
  ax5.set_ylabel('Count')
  ax5.set_title(f'Distribution of {col_name} in the dataset')
  tempo_np.hist(alpha=0.7, bins=30)
  if i == len:
    plt.tight_layout()

fig5 = plt.figure(figsize = (18,18))
col_name = ['danceability', 'duration_ms', 'acousticness', 'energy', 'instrumentalness', 'key', 'liveness', 'loudness', 'mode', 'popularity', 'speechiness', 'tempo', 'valence', 'year']
for i in range(len(col_name)):
  plot_grid(col_name=col_name[i], i=(i+1), len = len(col_name))


def plot_grid(col_name, i, len ):
'''Plot a grid of images corresponding to Distributions of popular. and unpopular songs w.r.t features'
'''
  happy = df_musical_features[df_musical_features[ 'valence'] > 0.5][col_name]
  sad = df_musical_features[df_musical_features[ 'valence'] <= 0.5][col_name]

  ax5 = fig6.add_subplot(5,3,i)
  ax5.set_xlabel(f'{col_name.capitalize()}')
  ax5.set_ylabel('Count')
  ax5.set_title(f'Distributions of haapy vs sad songs w.r.t {col_name}')
  happy.hist(alpha=0.5, bins=30, label=f'Happy-{col_name} dist.')
  sad.hist(alpha=0.5, bins=30, label=f'Sad-{col_name} dist.')
  plt.legend(loc='upper right')
  if i == len:
    plt.tight_layout()


fig6 = plt.figure(figsize = (18,18))
col_name = ['danceability', 'duration_ms', 'acousticness', 'energy', 'instrumentalness', 'key', 'liveness', 'loudness', 'mode', 'speechiness', 'tempo', 'popularity', 'year']
for i in range(len(col_name)):
  plot_grid(col_name=col_name[i], i=i+1, len = len(col_name))

# pop >= 50 and pop < 50
# Less_popular = df_musical_features[df_musical_features[ 'popularity'] <= 50][col_name]
# More_popular = df_musical_features[df_musical_features[ 'popularity'] > 50][col_name]


def plot_grid(col_name, i, len ):
    '''Plot a grid of images corresponding to Distributions of popular. and unpopular songs w.r.t features'
'''
  Popular = df_musical_features[df_musical_features[ 'popularity'] <= 50][col_name]
  Unpopular = df_musical_features[df_musical_features[ 'popularity'] > 50][col_name]

  ax5 = fig6.add_subplot(5,3,i)
  ax5.set_xlabel(f'{col_name.capitalize()}')
  ax5.set_ylabel('Count')
  ax5.set_title(f'Distributions of popular and unpopular songs w.r.t {col_name}')
  Popular.hist(alpha=0.5, bins=30, label=f'Popular {col_name} distribution')
  Unpopular.hist(alpha=0.5, bins=30, label=f'Unpopular {col_name} distribution')
  plt.legend(loc='upper right')
  if i == len:
    plt.tight_layout()


fig6 = plt.figure(figsize = (18,18))
col_name = ['danceability', 'duration_ms', 'acousticness', 'energy', 'instrumentalness', 'key', 'liveness', 'loudness', 'mode', 'speechiness', 'tempo', 'valence', 'year']
for i in range(len(col_name)):
  plot_grid(col_name=col_name[i], i=i+1, len = len(col_name))

