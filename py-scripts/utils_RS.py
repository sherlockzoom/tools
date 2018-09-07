import os
import numpy as np
from osgeo import gdal

def stretch_8bit(bands, lower_percent=2, higher_percent=98):
    # print(bands.shape)
    out = np.zeros_like(bands).astype(np.uint8)
    # for i in range(3):
    a = 0
    b = 255
    c = np.percentile(bands, lower_percent)
    d = np.percentile(bands, higher_percent)
    t = a + (bands - c) * (b - a) / (d - c)
    t[t<a] = a
    t[t>b] = b
    out[:,:] =t
    return out.astype(np.uint8)

def main():
    band_fn = ""
    in_ds = gdal.Open(band_fn)
    in_band_red = in_ds.GetRasterBand(1)  # red
    in_band_green = in_ds.GetRasterBand(2)
    in_band_blue = in_ds.GetRasterBand(3)

    in_band_lst = [in_band_red, in_band_green, in_band_blue]

    gtiff_driver = gdal.GetDriverByName('GTiff')
    out_ds = gtiff_driver.Create('rgb_8bit.tif',
                                 in_band_red.XSize, in_band_red.YSize, 3, in_band_red.DataType)

    out_ds.SetProjection(in_ds.GetProjection())
    out_ds.SetGeoTransform(in_ds.GetGeoTransform())

    for i, in_band in enumerate(in_band_lst):
        in_data = in_band.ReadAsArray()
        out_band = out_ds.GetRasterBand(i+1)
        out_band.WriteArray(in_data)
    out_ds.FlushCache()
    for i in range(1,4):
        out_ds.GetRasterBand(i).ComputeStatistics(False)

    out_ds.BuildOverviews("average", [2,4,8,16,32])
    del out_ds

if __name__ == '__main__':
    main()
