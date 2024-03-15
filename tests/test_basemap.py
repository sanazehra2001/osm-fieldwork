#!/usr/bin/python3

# Copyright (c) 2022, 2023 Humanitarian OpenStreetMap Team
#
# This file is part of osm_fieldwork.
#
#     Underpass is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     Underpass is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with osm_fieldwork.  If not, see <https:#www.gnu.org/licenses/>.
#
"""Test functionalty of basemapper.py."""

import logging
import os
import shutil
from io import BytesIO
from osm_fieldwork.basemapper import BaseMapper
from osm_fieldwork.basemapper import create_basemap_file
from osm_fieldwork.sqlite import DataFile

log = logging.getLogger(__name__)

rootdir = os.path.dirname(os.path.abspath(__file__))
boundary_file = f"{rootdir}/testdata/Rollinsville.geojson"

with open(boundary_file, "rb") as geojson_file:
    boundary = geojson_file.read()
boundary = BytesIO(boundary)

outfile = f"{rootdir}/testdata/rollinsville.mbtiles"
base = "./tiles"


def test_create():
    """See if the file got loaded."""
    hits = 0

    basemap = BaseMapper(boundary, base, "topo", False)
    tiles = list()
    for level in [8, 9, 10, 11, 12]:
        basemap.getTiles(level)
        tiles += basemap.tiles

    if len(tiles) == 5:
        hits += 1

    if tiles[0].x == 52 and tiles[1].y == 193 and tiles[2].x == 211:
        hits += 1

    outf = DataFile(outfile, basemap.getFormat())
    outf.writeTiles(tiles, base)

    outf.db.close()
    outf.db = None
    outf.cursor = None

    os.remove(outfile)
    shutil.rmtree(base)

    assert hits == 2


def clear_out_dir():

    print("\nDeleting all files and directories from tiles cache \n")

    for filename in os.listdir(base):
        file_path = os.path.join(base, filename)

        try:
            if os.path.isfile(file_path):
                os.remove(file_path)

            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)

        except Exception as e:
            print(f"Failed to delete {file_path}: {e}")


# Test create_basemap_file with Bbox Coordinates


def test_bbox_coords():
    boundary = "-4.730494, 41.650541, -4.725634, 41.652874"

    create_basemap_file(
        verbose=True,
        boundary=boundary,
        outfile=outfile,
        outdir=base,
        zooms="12-15",
        source="esri",
    )

    assert os.listdir(base), "No files were downloaded in the directory"
    assert os.path.isfile(outfile), "Output file not created"

    clear_out_dir()

    print("Test passed with boundary passed as coordinates \n")


# Test create_basemap_file with GeoJSON BytesIOWrapped file


def test_in_memory_geojson():
    boundary_file = f"{rootdir}/testdata/Rollinsville.geojson"

    with open(boundary_file, "rb") as geojson_file:
        boundary = geojson_file.read()

    boundary = BytesIO(boundary)  # add to a BytesIO wrapper

    create_basemap_file(
        verbose=True,
        boundary=boundary,
        outfile=outfile,
        outdir=base,
        zooms="12-15",
        source="esri",
    )

    assert os.listdir(base), "No files were downloaded in the directory"
    assert os.path.isfile(outfile), "Output file not created"

    clear_out_dir()

    print("Test passed with boundary passed as BytesIO wrapped file \n")


if __name__ == "__main__":

    test_create()

    test_bbox_coords()

    test_in_memory_geojson()
