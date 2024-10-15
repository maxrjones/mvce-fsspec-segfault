import earthaccess
import xarray as xr
from rasterio.warp import calculate_default_transform


def warp_resample(dataset):
    src = "s3://gesdisc-cumulus-prod-protected/GPM_L3/GPM_3IMERGDE.07/2002/06/3B-DAY-E.MS.MRG.3IMERG.20020601-S000000-E235959.V07B.nc4"
    dstSRS = "EPSG:3857"
    srcSRS = "EPSG:4326"
    width = height = 256
    te = [
        -20037508.342789244,
        -20037508.342789244,
        20037508.342789244,
        20037508.342789244,
    ]
    earthaccess.login()
    fs = earthaccess.get_s3fs_session(daac="GES_DISC")
    fsspec_caching = {
        "cache_type": "none",
    }
    with fs.open(src, **fsspec_caching) as f:
        da = xr.open_dataset(f, engine="h5netcdf", mask_and_scale=True)["precipitation"]
        da = da.rename({"lon": "x", "lat": "y"}).transpose("time", "y", "x")
        da = da.rio.write_crs(srcSRS)
        da = da.rio.clip_box(
            *te,
            crs=dstSRS,
        )
        dst_transform, w, h = calculate_default_transform(
            srcSRS,
            dstSRS,
            da.rio.width,
            da.rio.height,
            *da.rio.bounds(),
            dst_width=width,
            dst_height=height,
        )
        return da.rio.reproject(dstSRS, shape=(h, w), transform=dst_transform)


if __name__ == "__main__":
    da = warp_resample("gpm_imerg")
