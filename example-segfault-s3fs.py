import earthaccess
import xarray as xr


def transpose_dataset():
    src = "s3://gesdisc-cumulus-prod-protected/GPM_L3/GPM_3IMERGDE.07/2002/06/3B-DAY-E.MS.MRG.3IMERG.20020601-S000000-E235959.V07B.nc4"
    earthaccess.login()
    fs = earthaccess.get_s3fs_session(daac="GES_DISC")
    fsspec_caching = {
        "cache_type": "none",
    }
    with fs.open(src, **fsspec_caching) as f:
        da = xr.open_dataset(f, engine="h5netcdf", mask_and_scale=True)["precipitation"]
        da = da.rename({"lon": "x", "lat": "y"}).transpose("time", "y", "x")
        return da


if __name__ == "__main__":
    da = transpose_dataset()
