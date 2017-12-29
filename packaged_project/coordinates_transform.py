# ori author : https://gist.github.com/allieus/1180051/ab33229e820a5eb60f8c7971b8d1f1fc8f2cfabb

from pyproj import Proj
from pyproj import transform


WGS84 = { 'proj':'latlong', 'datum':'WGS84', 'ellps':'WGS84', }


# naver
TM128 = { 'proj':'tmerc', 'lat_0':'38N', 'lon_0':'128E', 'ellps':'bessel',
   'x_0':'400000', 'y_0':'600000', 'k':'0.9999',
   'towgs84':'-146.43,507.89,681.46'}


def xy_coordinates_transform_by_epsg_input(x, y, input_epsg, output_epsg):
    inProj = Proj(init='epsg:{}'.format(input_epsg))
    outProj = Proj(init='epsg:{}'.format(output_epsg))
    return transform(inProj, outProj, x, y)


def tm128_to_wgs84(x, y):
    return transform(Proj(**TM128), Proj(init='epsg:4326'), x, y )