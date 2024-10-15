import earthaccess
import fsspec
import xarray as xr
from rasterio.warp import calculate_default_transform


def download_dataset(dataset):
    earthaccess.login()
    results = earthaccess.search_data(
        concept_id="C2723754850-GES_DISC",
        count=1,
        temporal=("2002-06-01", "2002-06-01"),
    )
    earthaccess.download(results, "")[0]


def warp_resample(dataset):
    src = "3B-DAY-E.MS.MRG.3IMERG.20020601-S000000-E235959.V07B.nc4"
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
    fs = fsspec.filesystem("file")
    with fs.open(src) as f:
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
    dataset = "gpm_imerg"
    download_dataset(dataset)
    da = warp_resample(download_dataset)
