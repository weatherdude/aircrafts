def airtraffic(lat,lon):
    import math
    import numpy as np
    from opensky_api import OpenSkyApi
    # Calculate bounding box from center lat/lon coordinates
    #lat = math.radians(52.470868)
    #lon = math.radians(13.325687)
    lat = math.radians(lat)
    lon = math.radians(lon)

    distance = 30e3 # radius for the bounding box (m)
    R = 6371e3 # earth radius (m)
    Ad = distance/R # angular distance
    theta = np.array([math.radians(360), math.radians(90), math.radians(180), math.radians(270)]) # angles to lat/lon for bounding box

    lat2 = []
    lon2 = []
    for i in range(0,len(theta)):
        lat2.append(math.degrees(math.asin(math.sin(lat)*math.cos(Ad) + math.cos(lat)*math.sin(Ad)*math.cos(theta[i]))))
        lon2.append(math.degrees(lon + math.atan2(math.sin(theta[i])*math.sin(Ad)*math.cos(lat),math.cos(Ad)-math.sin(lat)*math.sin(lat2[i]))))

    min_lat = min(lat2)
    max_lat = max(lat2)
    min_lon = min(lon2)
    max_lon = max(lon2)

    api = OpenSkyApi()
    # bbox = (min latitude, max latitude, min longitude, max longitude)
    geo_altitude = []
    plane_lat = []
    plane_lon = []
    callsign = []
    velocity = []
    icao = []

    states = api.get_states(bbox=(min_lat, max_lat, min_lon, max_lon))
    for s in states.states:
        #print("(%r,%r, %r, %r, %r, %r, %r, %r)" % (s.icao24,s.callsign,s.origin_country,s.longitude, s.latitude, s.baro_altitude,s.geo_altitude, s.velocity))
        geo_altitude.append(s.geo_altitude) # (m)
        plane_lat.append(s.latitude)
        plane_lon.append(s.longitude)
        callsign.append(s.callsign)
        velocity.append(s.velocity) # (m/s)
        icao.append(s.icao24)
    return geo_altitude,plane_lat,plane_lon,callsign,velocity,icao