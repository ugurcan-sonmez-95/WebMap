import folium
import pandas

### Reads the data
data = pandas.read_csv("Volcanoes.txt")
lat = list(data["LAT"])
lon = list(data["LON"])
elev = list(data["ELEV"])
name = list(data["NAME"])

### Shows the color of volcanoes according to their heights
def color_picker(elevation):
    if elevation < 1000:
        return 'green'
    elif 1000 <= elevation < 3000:
        return 'orange'
    else:
        return 'red'

### Popup html
html = """Volcano name:<br>
<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Height: %s m
"""

### The map
map = folium.Map(location = [39.740124, -104.993395], zoom_start = 3, tiles = "Stamen Terrain")

### Volcanoes layer
fgv = folium.FeatureGroup(name = "Volcanoes")

for lt, ln, el, name in zip(lat, lon, elev, name):
    iframe = folium.IFrame(html = html %(name,name,el), width = 150, height = 80)
    fgv.add_child(folium.CircleMarker(location = [lt, ln], radius = 6, popup = folium.Popup(iframe), fill_color = color_picker(el), color = 'grey', fill_opacity = 0.7, fill = True))

### Population layer
fgp = folium.FeatureGroup(name = "Population")

fgp.add_child(folium.GeoJson(data = open('world.json', 'r', encoding = 'utf-8-sig').read(), style_function = lambda x: {'fillColor':'green' if x['properties']['POP2005'] < 10000000 else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000 else 'red'}))

### Adds the layers to the map
map.add_child(fgv)
map.add_child(fgp)
### Adds a layer control panel
map.add_child(folium.LayerControl())

### Saves the changes on the map
map.save("Map1.html")