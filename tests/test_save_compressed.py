import os

import pytest
import xarray as xr

import bitinformation_pipeline as bp


@pytest.mark.parametrize("for_cdo", [True, False])
def test_get_compress_encoding_for_cdo(rasm, for_cdo):
    ds = rasm
    encoding = bp.get_compress_encoding(ds, for_cdo=for_cdo)
    v = list(ds.data_vars)[0]
    time_axis = ds[v].get_axis_num("time")
    if for_cdo:
        assert encoding[v]["chunksizes"][time_axis] == 1
    else:
        assert encoding[v]["chunksizes"][time_axis] > 1


@pytest.mark.parametrize("dask", [True, False])
def test_to_compressed_netcdf(rasm, dask):
    """Test to_compressed_netcdf reduces size on disk."""
    ds = rasm
    if dask:
        ds = ds.chunk("auto")
    label = "file"
    # save
    ds.to_netcdf(f"{label}.nc")
    ds.to_compressed_netcdf(f"{label}_compressed.nc")
    # check size reduction
    ori_size = os.path.getsize(f"{label}.nc")
    compressed_size = os.path.getsize(f"{label}_compressed.nc")
    assert compressed_size < ori_size


def test_to_compressed_netcdf_for_cdo_no_time_dim_var(air_temperature):
    """Test to_compressed_netcdf if `for_cdo=True` and one var without `time_dim`."""
    ds = air_temperature
    ds["air_mean"] = ds["air"].isel(time=0)
    ds.to_compressed_netcdf("test.nc", for_cdo=True)
    os.remove("test.nc")
