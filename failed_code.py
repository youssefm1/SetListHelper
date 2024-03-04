def convert_spotify_key_to_camelot(spotify_key, mode):
    camelot_mapping_minor = {0: '5A', 1: '12A', 2: '7A', 3: '2A', 4: '9A', 5: '4A', 6: '11A', 7: '6A', 8: '1A', 9: '8A', 10: '3A', 11: '10A'}
    camelot_mapping_major = {0: '8B', 1: '3B', 2: '10B', 3: '5B', 4: '12B', 5: '7B', 6: '2B', 7: '9B', 8: '4B', 9: '11B', 10: '6B', 11: '1B'}

    if spotify_key not in camelot_mapping_major or spotify_key not in camelot_mapping_minor:
        
        app.logger.info(spotify_key)
        return None

    return camelot_mapping_major[spotify_key] if mode == 1 else camelot_mapping_minor[spotify_key]

def are_keys_compatible(spotify_key1, spotify_mode1, spotify_key2, spotify_mode2):
    # Convert Spotify keys to Camelot Wheel notation
    camelot_key1 = convert_spotify_key_to_camelot(spotify_key1, spotify_mode1)
    camelot_key2 = convert_spotify_key_to_camelot(spotify_key2, spotify_mode2)

    # Check compatibility based on Camelot Wheel principles
    if camelot_key1 == None or camelot_key2 == None: 
        return None
    app.logger.info(abs(int(camelot_key1[:-1]) - int(camelot_key2[:-1])))
    return abs(int(camelot_key1[:-1]) - int(camelot_key2[:-1])) % 12 in {0, 1, 2, 11}

