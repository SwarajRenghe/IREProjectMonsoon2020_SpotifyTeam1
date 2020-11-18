# Spotify Recommender System 

# Setup & Running

Run the following set of commands to start the playlist generator

```
cd searching/advanced 
python3 gen_playlist.py
```

This will start the the CLI application. 

# Generating a Playlist

There are 4 types of searches that this playlist generator supports

* **Similarity based** : Enter the URI of the query song
* **Dissimilarity based** : Enter the URI of the query song
* **Field based** : Enter the musical feature field followed by <num, #number> or <id, URI> for the song or value with respect to which the playlist is to be generated
* **Mood based** : Enter the mood cluster name *(for eg : mood0)*

# References

### Network Embeddings 
LINE (Large-scale Information Network Embedding) algorithm. <br>
Reference : https://github.com/shenweichen/GraphEmbedding <br>
Reference Paper : [LINE](https://arxiv.org/pdf/1503.03578.pdf) <br>




