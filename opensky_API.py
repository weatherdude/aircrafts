import math
import cv2
from PIL import Image
from PIL import ImageDraw
import numpy as np
from opensky_api import OpenSkyApi
from aircraft_type import aircraft_type_search

# define functions
def coords_from_zenith_azimuth(rows,cols,zenith,azimuth):
    import math
    # rows: number of rows in image
    # cols: number of columns in image
    # zenith: zenith angle (°)
    # azimuth: azimuth angle (°) - 0° = north , 90° = east

    center_px = (math.floor(rows/2),math.floor(cols/2))
    tau = rows/180 # scale factor (px/°)

    d = zenith * tau # distance in px
    azimuth_rad = (azimuth-90) / 180 * math.pi

    x = math.floor(center_px[0] + d * math.cos(azimuth_rad))
    y = math.floor(center_px[1] + d * math.sin(azimuth_rad))

    return x,y

# Calculate bounding box from center lat/lon coordinates
lat = math.radians(34.695681)
lon = math.radians(-86.669805)

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
    geo_altitude.append(s.geo_altitude)
    plane_lat.append(s.latitude)
    plane_lon.append(s.longitude)
    callsign.append(s.callsign)
    velocity.append(s.velocity)
    icao.append(s.icao24)

# visualize location on fisheye view of station
# main part
path = r'C:\Users\Admin\Documents\UFO\Satellites\sky_circle.png'

image = cv2.imread(path, 1)
rows,cols,channels = image.shape

img1 = Image.open(path)

path = r"C:\Users\Admin\Documents\UFO\Opensky\plane_icon.png"
img2 = Image.open(path) #.convert("RGBA")

for i in range(0,len(geo_altitude)):
    # calculate horizontal distance between plane and station coordinates (haversine formula)
    plane_lat_rad = math.radians(plane_lat[i])
    plane_lon_rad = math.radians(plane_lon[i])
    delta_lat = plane_lat_rad - lat
    delta_lon = plane_lon_rad - lon
    a = math.sin(delta_lat/2) * math.sin(delta_lat/2) + math.cos(lat) * math.cos(plane_lat_rad) \
    * math.sin(delta_lon/2)*math.sin(delta_lon/2)
    c = 2 * math.atan2(math.sqrt(a),math.sqrt(1-a))
    horz_dist = R * c

    elevation_angle = math.degrees(math.atan(geo_altitude[i] / horz_dist))
    zenith = 90-elevation_angle

    # calculate bearing between station and plane
    dL = plane_lon_rad-lon
    X = math.cos(plane_lat_rad) * math.sin(dL)
    Y = math.cos(lat)*math.sin(plane_lat_rad) - math.sin(lat)*math.cos(plane_lat_rad)*math.cos(dL)
    azimuth = math.degrees(math.atan2(X,Y))
    if azimuth < 0:
        azimuth = math.degrees(math.radians(azimuth)+2*math.pi)

    # get pixel coordinates
    x,y = coords_from_zenith_azimuth(rows,cols,zenith,azimuth)

    # Pasting img2 image on top of img1
    # starting at coordinates (0, 0)
    img1.paste(img2, (x,y), mask = img2)
    # Call draw Method to add 2D graphics in an image
    I1 = ImageDraw.Draw(img1)

    height = geo_altitude[i]/1000 # height of plane (km)
    speed_kmh = velocity[i]*3.6 # speed of plane (km/h)
    speed_mh = velocity[i]*2.237 # speed of plane (miles/h)

    # get the aircraft type from local FAA database
    type_aircraft = aircraft_type_search(icao[i])

    # Add Text to an image
    if x+107 > cols: # to avoid that the textbox extends out of the image
        x = x - ((x+107)-cols)
    I1.multiline_text((x, y + 25), "Callsign: "+callsign[i] + "\n" + "Speed: " + str(round(speed_kmh,2)) + " km/h" + "\n" + "Height: " + str(round(height,2)) + " km" + "\n" + "Aircraft type: " + type_aircraft, fill=(150, 0, 0))
# Displaying the image
img1.show()
img1.save("planes_result.png")
