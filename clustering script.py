from sklearn.cluster import KMeans
import numpy as np
from itertools import combinations

# Your list of songs
songs = [
{
    "energy": 0.358,
    "key": 7,
    "name": "Mustafa (southbank)",
    "tempo": 121.985
  },
  {
    "energy": 0.0544,
    "key": 4,
    "name": "Silence",
    "tempo": 115.393
  },
  {
    "energy": 0.0131,
    "key": 7,
    "name": "Eyelar (stamford street)",
    "tempo": 93.113
  },
  {
    "energy": 0.0257,
    "key": 4,
    "name": "Distance",
    "tempo": 113.157
  },
  {
    "energy": 0.192,
    "key": 4,
    "name": "J'y suis jamais all\u00e9 - From ''Amelie''",
    "tempo": 105.052
  },
  {
    "energy": 0.685,
    "key": 8,
    "name": "Bleu (better with time)",
    "tempo": 121.928
  },
  {
    "energy": 0.0991,
    "key": 8,
    "name": "Back in Time",
    "tempo": 159.892
  }]


def are_keys_compatible(key1, key2):
    return abs(key1 - key2) % 12 in {0, 1, 2, 11}

def are_tempos_compatible(tempo1, tempo2):
    tempo1, tempo2 = max(tempo1, tempo2), min(tempo1, tempo2)
    tempo_dif = tempo1 - tempo2
    if tempo_dif >= 10 and (abs(tempo_dif-tempo2)) >= 10:
        return False
    return True


def group_songs(songs):
    grouped_songs = []

    for song in songs:
        added = False
        for group in grouped_songs:
            if all(are_keys_compatible(song["key"], other_song["key"]) and
                   are_tempos_compatible(song["tempo"], other_song["tempo"])
                   for other_song in group):
                group.append(song)
                added = True
                break

        if not added:
            grouped_songs.append([song])
    grouped_songs = [group for group in grouped_songs if len(group) > 1]

    return grouped_songs


# Example usage
grouped_songs = group_songs(songs)
print(grouped_songs)
# Output the grouped songs
for i, group in enumerate(grouped_songs, 1):
    print(f"Group {i}:")
    for song_name in group:
        print(f"  - {song_name}")
    print("\n")
