# downloading 2 python libraries to make simple webmap !!

# folium ----- Folium is a Python library that makes it possible visualize data on an interactive Leaflet map.

# pandas ----- pandas is a fast, powerful, flexible and easy to use open source data analysis and manipulation tool,
# built on top of the Python programming language.

# _______________** CODE STARTS **_______________

import folium
import pandas

data = pandas.read_excel("iit_data.xlsx")
# , encoding="unicode_escape"
iit_ranking = list(data["IIT Ranking"])
College_name = list(data["IIT College"])
NIRF_score = list(data["NIRF Score"])
Latitude_location = list(data["Latitude"])
Longitude_location = list(data["Longitude"])
images = list(data["Image"])

# parent map
folium_map = folium.FeatureGroup("map")

# utf is uniform transformation format
# 8 stands for 8 bit
# and sig stands for signature and it is used because it treats file
# as BOM-bill of material(centralised source of information used to
# manufacture a product) information instead of string

folium_map.add_child(folium.GeoJson(data=(open("india_states.json", "r", encoding="utf-8-sig").read())))

# html code is to use the data set
for ranks, clg, score, lati, longi, ima in zip(iit_ranking, College_name, NIRF_score, Latitude_location, Longitude_location, images):
    folium_map.add_child(folium.Marker(location=[lati, longi], popup="<b> College Name : </b>" + str(clg) +
                                                                    "<br> <b> Rank among IIT's in India: </b>" + str(ranks) +
                         "<br> <b> NIRF Score : </b> " + str(score) +
                         "<br> <img src = "+ima+" height = 140, width = 280>", icon=folium.Icon(color="red")))

# location here is latitude and longitude of location from where
# the map starts its visibility
map_by_folium = folium.Map(location=[20.0000, 75.0000], zoom_start= 4)
map_by_folium.add_child(folium_map)

# saving this work as a html file where the json file consisting
# all the locations is downloaded from the internet
map_by_folium.save("final_map.html")

# now putting the data from excel sheet into the map



# _______________** CODE ENDS **_______________