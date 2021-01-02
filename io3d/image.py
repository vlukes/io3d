#! /usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Union
import numpy as np

class DataPlus(dict):

    @property
    def voxelsize_mm(self):
        return self["voxelsize_mm"]

    @voxelsize_mm.setter
    def voxelsize_mm(self, voxelsize_mm):
        self["voxelsize_mm"] = voxelsize_mm

    @property
    def data3d(self):
        return self["data3d"]

    @data3d.setter
    def data3d(self, value):
        self["data3d"] = value

    @property
    def segmentation(self):
        return self["segmentation"]

    @segmentation.setter
    def segmentation(self, value):
        self["segmentation"] = value

    @property
    def slab(self):
        return self["slab"]

    @slab.setter
    def slab(self, value):
        self["slab"] = value

    @property
    def orientation_axcodes(self):
        return self["orientation_axcodes"]

    @slab.setter
    def orientation_axcodes(self, value):
        self["orientation_axcodes"] = value

    def transform_orientation(self, axcodes):
        # if "orientations_axcodes" in self.keys():
        input_axcodes = self["orientation_axcodes"]
        self["data3d"] = transform_orientation(self["data3d"], input_axcodes, axcodes)
        self["orientation_axcodes"] = axcodes

    # def __getattr__(self, attr):
    #     print(f"attr: {attr}")
    #     return self[attr]
    #     # KeyError
    #
    # def __setattr__(self, attr, value):
    #     print(f"attr: {attr}: {value}")
    #     self[attr] = value


def as_datap(obj:Union[dict,DataPlus])->DataPlus:
    """
    Convert dict to DataPlus format if necessary.
    :param obj:
    :return:
    """
    if type(obj) == DataPlus:
        return obj
    elif type(obj) == dict:
        return DataPlus(obj)
    elif obj is None:
        return None
    else:
        raise TypeError("Type Dict or type DataPlus expected.")


def transform_orientation(arr:np.ndarray, input_axcodes, output_axcodes):
    """
    Change the orientation of the array. Most used axcodes are LPS (Left, Posterior and Superior) and RAS (Right,
    Anterior and Superior).  First letters of words Left, Right, Superior,
    Inferior, Anterior and Posterior can be used to describe anatomical orientation.
    To describe common orientation can be used words Left, Right, Up, Down, Front and Back.
    Left means from right to left, Superior means from inferior to superior.

    NiBabel package is used internally (https://nipy.org/nibabel/reference/nibabel.orientations.html)

    :param arr: input numpy array
    :param input_axcodes: Three letters describing the axis orientation. 'LPS' and 'RAS' are most common codes.
    :param output_axcodes:Three letters describing the axis orientation. 'LPS' and 'RAS' are most common codes.
    :return: transformed array
    """

    # ║ Common ║ Anatomical ║
    # ╠════════╬════════════╣
    # ║ Left   ║ Left       ║
    # ║ Right  ║ Right      ║
    # ║ Up     ║ Superior   ║
    # ║ Down   ║ Inferior   ║
    # ║ Front  ║ Anterior   ║
    # ║ Back   ║ Posterior
    import nibabel
    ornt_my = nibabel.orientations.axcodes2ornt(input_axcodes)
    ornt_ras = nibabel.orientations.axcodes2ornt(output_axcodes)
    ornt = nibabel.orientations.ornt_transform(ornt_my, ornt_ras)
    data3d_ornt = nibabel.orientations.apply_orientation(arr, ornt)
    return data3d_ornt