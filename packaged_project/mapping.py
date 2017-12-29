import folium
import pyproj
import shapely
import shapely.ops as ops
from shapely.geometry import Point, LineString, Polygon, MultiPoint, MultiLineString, MultiPolygon
import vincent
from vincent import AxisProperties, PropertySet, ValueRef

import pandas as pd
import numpy as np
import geopandas as gpd
from geopandas import GeoDataFrame

import os
from functools import partial


def df_to_gdf_with_lon_lat_point(df):
    geometry = [Point(xy) for xy in zip(df.longitude, df.latitude)]
    crs = {'init': 'epsg:4326'}
    gdf = GeoDataFrame(df, crs=crs, geometry=geometry)
    return gdf


def divide_gdf(gdf, labels):
    gdf['label'] = labels
    clustered_gdf = gdf.loc[gdf['label'] != -1, :]
    outliers_gdf = gdf.loc[gdf['label'] == -1, :]
    return clustered_gdf, outliers_gdf



class GeoProcessing(object):
    def __init__(self):
        pass

    def get_meter_square_area(self, polygon):
        geom = polygon
        geom_area = ops.transform(
            partial(
                pyproj.transform,
                pyproj.Proj(init='EPSG:4326'),
                pyproj.Proj(
                    proj='aea',
                    lat1=geom.bounds[1],
                    lat2=geom.bounds[3])),
            geom)
        return geom_area.area / 1000000

    def get_clus_polygon_gdf(self, gdf):
        pointlist_gdf = gpd.GeoDataFrame(gdf.groupby('label')['geometry'].apply(list))
        multipoint_gdf = gpd.GeoDataFrame(pointlist_gdf.geometry.apply(lambda x : MultiPoint(x)))
        polygon_gdf = gpd.GeoDataFrame(multipoint_gdf.geometry.apply(lambda x : x.convex_hull).values)
        polygon_gdf.columns = ['geometry']

        polygon_gdf['count'] = gdf.groupby('label').count().loc[:, 'longitude'].values
        polygon_gdf['area'] = polygon_gdf.geometry.apply(lambda x : self.get_meter_square_area(x))
        polygon_gdf['density'] = polygon_gdf['area'] / polygon_gdf['count']
        polygon_gdf['centroid'] = polygon_gdf.geometry.centroid.apply(lambda x : x.coords[0])
        return polygon_gdf


def get_clus_pivot_count_df(gdf, column=None):
    return gdf.groupby(['label', column]).count().pivot_table('geometry', 'label', column).fillna(0)


def slicer(criteria_df, additional_df_1, additional_df_2, column_name=None, method='numeric', _range=None, up_limit=None, down_limit=None):
    """slice criteria_df by method and get a piece of _range
       column_name : slicing criteria
       method : numeric or boolean or sort
       _range : up, down, mid for numeric
                specific str for boolean
                None for sort (up_limit needed)
       result : polygon criteria_df, feature df
    """
    target_idx = None
    if method == 'numeric':
        if _range == 'up':
            assert up_limit
            assert type(up_limit) is int or float
            try:
                target_idx = criteria_df.loc[criteria_df[column_name] >= up_limit, :].index
            except KeyError:
                print("Please check your column_name or limit")

        elif _range == 'down':
            assert down_limit
            assert type(down_limit) is int or float
            try:
                target_idx = criteria_df.loc[criteria_df[column_name] < down_limit, :].index
            except KeyError:
                print("Please check your column_name or limit")

        elif _range == 'mid':
            assert up_limit
            assert down_limit
            assert type(up_limit) is int or float
            assert type(down_limit) is int or float
            try:
                target_idx = criteria_df.loc[(criteria_df[column_name] < up_limit) & (criteria_df[column_name] >= down_limit), :].index
            except KeyError:
                print("Please check your column_name or limit")

        else:
            raise ValueError("You must input _range 'up' or 'down' or 'mid'.")

    elif method == 'boolean':
        try:
            target_idx = criteria_df.loc[criteria_df[column_name] == _range, :].index
        except KeyError:
            print("Please check your column_name or _range")
    elif method == 'sort':
        assert type(up_limit) is int
        try:
            target_idx = criteria_df.sort_values(column_name, ascending=False).iloc[:up_limit, :].index
        except KeyError:
            print("Please check your column_name or _range")
    else:
        raise ValueError("You must input a method 'numeric' xor 'boolean'.")
    sliced_criteria_df = criteria_df.loc[target_idx, :]
    sliced_additional_df_1 = additional_df_1.loc[target_idx, :]
    sliced_additional_df_2 = additional_df_2.loc[target_idx, :]
    return sliced_criteria_df, sliced_additional_df_1, sliced_additional_df_2

class BarPopMapping(object):
    def __init__(self):
        pass

    def get_vincent_bar_chart(self, target_df, idx):
        total = target_df.loc[idx, :].sum()
        target_df = pd.DataFrame({'count': target_df.loc[idx, :].sort_values(ascending=False)[:20]})
        vis = vincent.Bar(target_df['count'])
        vis.axes[0].properties = AxisProperties(
            labels=PropertySet(
                angle=ValueRef(value=45),
                align=ValueRef(value='left')
                )
            )
        vis.axis_titles(x= '', y='Count of Main 20 Category / Total : {}'.format(int(total)))
        vis.width = 300
        vis.height = 170
        # vis.padding['bottom'] = 90
        return vis.to_json()

    def get_polygons_layer(self, clus_polygon_gdf, clus_category_df, layer_name=None, marker_color='#43d9de'):
        clus_polygon_gdf_json = clus_polygon_gdf.to_json()
        layer = folium.GeoJson(clus_polygon_gdf_json, name=layer_name)

        taret_idx = clus_polygon_gdf.index
        target_df = clus_category_df.loc[taret_idx, :]

        for idx in taret_idx:
            folium.RegularPolygonMarker(
            list(clus_polygon_gdf.loc[idx, 'centroid'])[::-1],
            fill_color=marker_color,
            radius=6,
            popup=folium.Popup(max_width=400).add_child(
                folium.Vega(self.get_vincent_bar_chart(target_df, idx), width=400, height=270))
            ).add_to(layer)
        return layer


def slice_to_map(polygon_gdf, query_count_df, category_count_df, _slice=True,
                     criteria='geometry', column_name=None, method='numeric', _range='up', up_limit=1.0, down_limit=None,
                     layer_name=None, marker_color='#3139cc', zoom_start=11,
                     visualization=None, out_fp='./'):
    if _slice:
        if criteria == 'geometry':
            target_gdf, target_q_df, target_c_df = slicer(polygon_gdf,
                                            query_count_df,
                                            category_count_df,
                                            column_name=column_name,
                                            method=method,
                                            _range=_range,
                                            up_limit=up_limit,
                                            down_limit=down_limit)
        elif criteria == 'query':
            target_q_df, target_gdf, target_c_df = slicer(query_count_df,
                                            polygon_gdf,
                                            category_count_df,
                                            column_name=column_name,
                                            method=method,
                                            _range=_range,
                                            up_limit=up_limit,
                                            down_limit=down_limit)
        elif criteria == 'category':
            target_c_df, target_gdf, target_q_df = slicer(category_count_df,
                                            polygon_gdf,
                                            query_count_df,
                                            column_name=column_name,
                                            method=method,
                                            _range=_range,
                                            up_limit=up_limit,
                                            down_limit=down_limit)
        else:
            raise ValueError("Unvalid input for criteria!")
    else:
        target_gdf = polygon_gdf
        target_q_df = query_count_df
        target_c_df = category_count_df

    if visualization == 'query':
        layer = BarPopMapping().get_polygons_layer(target_gdf,
                                   target_q_df,
                                   layer_name=layer_name,
                                   marker_color=marker_color)
    elif visualization == 'category':
        layer = BarPopMapping().get_polygons_layer(target_gdf,
                                   target_c_df,
                                   layer_name=layer_name,
                                   marker_color=marker_color)
    else:
        raise ValueError("Unvalid input for visualization!")
    # base mapping
    lat, lon = 37.54, 126.99
    m = folium.Map([lat, lon],
                   tiles='OpenStreetMap',
                   zoom_start=zoom_start,
                   control_scale=True)

    m.add_child(layer)
    folium.LayerControl().add_to(m)
    m.save(os.path.join(out_fp, layer_name) + '.html')