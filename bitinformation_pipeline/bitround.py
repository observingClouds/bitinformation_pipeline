import xarray as xr
from dask import is_dask_collection
from numcodecs.bitround import BitRound

from .bitinformation_pipeline import _jl_bitround, get_keepbits


def _np_bitround(data, keepbits):
    """Bitround for Arrays."""
    codec = BitRound(keepbits=keepbits)
    data = data.copy()  # otherwise overwrites the input
    encoded = codec.encode(data)
    return codec.decode(encoded)


def xr_bitround(da, keepbits):
    """Apply bitrounding based on keepbits from bp.get_keepbits for xarray.Dataset or xr.DataArray wrapping numcodecs.bitround

    Inputs
    ------
    da : xr.DataArray or xr.Dataset
      input data to bitround
    keepbits : int or dict of {str: int}
      how many bits to keep as int

    Returns
    -------
    da_bitrounded : xr.DataArray or xr.Dataset

    Example
    -------
        >>> ds = xr.tutorial.load_dataset("air_temperature")
        >>> info_per_bit = bp.get_bitinformation(ds, dim="lon")
        >>> keepbits = bp.get_keepbits(info_per_bit, 0.99)
        >>> ds_bitrounded = bp.xr_bitround(ds, keepbits)
    """
    if isinstance(da, xr.Dataset):
        da_bitrounded = da.copy()
        for v in da.data_vars:
            da_bitrounded[v] = xr_bitround(da[v], keepbits)
        return da_bitrounded

    assert isinstance(da, xr.DataArray)
    if isinstance(keepbits, int):
        keep = keepbits
    elif isinstance(keepbits, dict):
        v = da.name
        if v in keepbits.keys():
            keep = keepbits[v]
        else:
            raise ValueError(f"name {v} not for in keepbits: {keepbits.keys()}")
    da = xr.apply_ufunc(_np_bitround, da, keep, dask="parallelized", keep_attrs=True)
    da.attrs["_QuantizeBitRoundNumberOfSignificantDigits"] = keep
    return da


def jl_bitround(da, keepbits):
    """Apply bitrounding based on keepbits from bp.get_keepbits for xarray.Dataset or xr.DataArray wrapping BitInformation.jl.round.

    Inputs
    ------
    da : xr.DataArray or xr.Dataset
      input data to bitround
    keepbits : int or dict of {str: int}
      how many bits to keep as int

    Returns
    -------
    da_bitrounded : xr.DataArray or xr.Dataset

    Example
    -------
        >>> ds = xr.tutorial.load_dataset("air_temperature")
        >>> info_per_bit = bp.get_bitinformation(ds, dim="lon")
        >>> keepbits = bp.get_keepbits(info_per_bit, 0.99)
        >>> ds_bitrounded = bp.jl_bitround(ds, keepbits)
    """
    if isinstance(da, xr.Dataset):
        da_bitrounded = da.copy()
        for v in da.data_vars:
            da_bitrounded[v] = jl_bitround(da[v], keepbits)
        return da_bitrounded

    assert isinstance(da, xr.DataArray)
    if isinstance(keepbits, int):
        keep = keepbits
    elif isinstance(keepbits, dict):
        v = da.name
        if v in keepbits.keys():
            keep = keepbits[v]
        else:
            raise ValueError(f"name {v} not for in keepbits: {keepbits.keys()}")
    da = xr.apply_ufunc(_jl_bitround, da, keep, dask="forbidden", keep_attrs=True)
    da.attrs["_QuantizeBitRoundNumberOfSignificantDigits"] = keep
    return da


def bitround_along_dim(
    ds, info_per_bit, dim, inflevels=[1.0, 0.9999, 0.99, 0.975, 0.95]
):
    """
    Apply bitrounding on slices along dim based on inflevels.
    Helper function to generate data for Fig. 3 in Klöwer et al. 2021.

    Klöwer, M., Razinger, M., Dominguez, J. J., Düben, P. D., & Palmer, T. N. (2021). Compressing atmospheric data into its real information content. Nature Computational Science, 1(11), 713–724. doi: 10/gnm4jj

    Inputs
    ------
    ds : xr.Dataset, xr.DataArray
      input
    info_per_bit : dict
      Information content of each bit for each variable in ds. This is the output from get_bitinformation.
    dim : str
      name of dimension for slicing
    inflevels : list of floats
      Level of information that shall be preserved. Defaults to [1.0, 0.9999, 0.99, 0.975, 0.95].

    Returns
    -------
    ds : xr.Dataset, xr.DataArray
      bitrounded on slices along dim based on inflevels

    Example
    -------
    >>> ds = xr.tutorial.load_dataset("air_temperature")
    >>> info_per_bit = bp.get_bitinformation(ds, dim="lon")
    >>> ds_bitrounded_along_lon = bp.bitround.bitround_along_dim(
    ...     ds, info_per_bit, dim="lon"
    ... )
    >>> (ds - ds_bitrounded_along_lon)["air"].isel(time=0).plot()  # doctest: +ELLIPSIS
    <matplotlib.collections.QuadMesh object at ...>
    """
    stride = ds[dim].size // len(inflevels)
    new_ds = []
    for i, inf in enumerate(inflevels):  # last slice might be a bit larger
        ds_slice = ds.isel(
            {
                dim: slice(
                    stride * i, stride * (i + 1) if i != len(inflevels) - 1 else None
                )
            }
        )
        keepbits_slice = get_keepbits(info_per_bit, inf)
        if inf != 1:
            ds_slice_bitrounded = xr_bitround(ds_slice, keepbits_slice)
        else:
            ds_slice_bitrounded = ds_slice
        new_ds.append(ds_slice_bitrounded)
    return xr.concat(new_ds, dim)
