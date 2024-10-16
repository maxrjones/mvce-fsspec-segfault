import earthaccess
import xarray as xr


def download_dataset():
    earthaccess.login()
    results = earthaccess.search_data(
        concept_id="C2723754850-GES_DISC",
        count=1,
        temporal=("2002-06-01", "2002-06-01"),
    )
    earthaccess.download(results, "")[0]


def transpose_dataset():
    src = "3B-DAY-E.MS.MRG.3IMERG.20020601-S000000-E235959.V07B.nc4"
    da = xr.open_dataset(src, engine="h5netcdf", mask_and_scale=True)["precipitation"]
    da = da.rename({"lon": "x", "lat": "y"}).transpose("time", "y", "x")
    return da


if __name__ == "__main__":
    download_dataset()
    da = transpose_dataset()
