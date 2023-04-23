import requests
import xml.etree.ElementTree as ET

units = 'SI' # otherwise imperial

# Define the coordinates of the LON-LAT rectangle
min_lon = "13.095"
max_lon = "13.704"
min_lat = "52.35"
max_lat = "52.68"

# Define the URL for the METAR weather data request with cloud base height
url = f"https://www.aviationweather.gov/adds/dataserver_current/httpparam?dataSource=metars&requestType=retrieve&format=xml&minLon={min_lon}&maxLon={max_lon}&minLat={min_lat}&maxLat={max_lat}&hoursBeforeNow=1&mostRecentForEachStation=true&fields=sky_cover,cloud_base_ft_agl"

# Send the request to aviationweather.gov and get the response
response = requests.get(url)

# Parse the response XML and extract the cloud base height
root = ET.fromstring(response.content)
cloud_base_height = []
sky_cover = []
for metar in root.iter('METAR'):
    for cloud_base in metar.iter('sky_condition'):
        if 'cloud_base_ft_agl' in cloud_base.attrib:
            cloud_base_ft_agl = int(cloud_base.attrib['cloud_base_ft_agl'])
            if units == 'SI':
                cloud_base_height.append(round(cloud_base_ft_agl * 0.3048, 2))
            else:
                cloud_base_height.append(cloud_base_ft_agl)
        if 'sky_cover' in cloud_base.attrib:
            sky_cover_abbr = cloud_base.attrib['sky_cover']
            if sky_cover_abbr == 'SKC' or sky_cover_abbr == 'CLR':
                sky_cover.append('Clear')
            elif sky_cover_abbr == 'FEW':
                sky_cover.append('Few')
            elif sky_cover_abbr == 'SCT':
                sky_cover.append('Scattered')
            elif sky_cover_abbr == 'BKN':
                sky_cover.append('Broken')
            elif sky_cover_abbr == 'OVC':
                sky_cover.append('Overcast')


# Print the list of cloud base heights
#print(response.content)
print(cloud_base_height)
print(sky_cover)