from io import BytesIO
from osm_fieldwork.basemapper import create_basemap_file

with open("osm_fieldwork\\..\\tests\\testdata\\Rollinsville.geojson", "rb") as geojson_file:
    boundary = geojson_file.read() 
    boundary_bytesio = BytesIO(boundary)   # add to a BytesIO wrapper

create_basemap_file(
    verbose=True,
    boundary=boundary_bytesio,
    outfile="outreachy.mbtiles",
    zooms="12-15",
    source="esri",
)