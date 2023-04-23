# aircrafts
The script **opensky_API.py** calls the opensky API and calculates a bounding box from central lat/lon coordinates and a given radius. The position of all aircrafts within this bounding box will be returned and visualized for a fisheye view of the upper hemisphere.

The script **airtraffic.py** contains a function that calls the opensky API with a given latitude,longitude pair and returns lists with airtraffic data within a radius of 30 km.

The script **weather_METAR.py** allows to request cloud base height in m or ft within a latitude/longitude rectangle.
