from pygeodesy import geohash


geohash_data = {}

def calculate_geohashes(lats, lons, precision):
    hashes = []
    for lat, lon in zip(lats, lons):
        if (lat, lon, precision) in geohash_data:
            h = geohash_data[(lat, lon, precision)]
        else:
            h = geohash.encode(lat, lon, precision)
            geohash_data[(lat, lon, precision)] = h
        hashes.append(h)
    return hashes