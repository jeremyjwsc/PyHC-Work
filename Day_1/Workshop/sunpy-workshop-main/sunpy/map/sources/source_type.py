"""
Source type-dependencies.

Helioviewer JPEG2000 files have stretched images compared to the FITS data.

"""
from astropy.visualization import LinearStretch

__author__ = "Jack Ireland"
__email__ = "jack.ireland@nasa.gov"

__all__ = ['from_helioviewer_project', 'source_stretch']


def from_helioviewer_project(meta):
    """
    Test determining if the given metadata contains Helioviewer Project sourced data.

    Parameters
    ----------
    meta : `~astropy.utils.metadata.MetaData`
        The metadata to parse.

    Returns
    -------
    If the data of the map comes from the Helioviewer Project, then True is
    returned. If not, False is returned.
    """
    return 'helioviewer' in meta.keys()


def source_stretch(meta, fits_stretch):
    """
    Assign the correct source-dependent image stretching function.

    Parameters
    ----------
    meta : `~astropy.utils.metadata.MetaData`
        The metadata to parse.
    fits_stretch : `~astropy.visualization.BaseStretch`
        Image stretching function used when the source image data comes from a
        FITS file.

    Returns
    -------
    An image stretching function appropriate to the image data source.
    """
    if from_helioviewer_project(meta):
        # Helioviewer JPEG2000 files already have a stretched data values, so
        # just use a linear stretch.
        return LinearStretch()
    else:
        # Not a Helioviewer JPEG2000 file, so assume the data has not been
        # stretched and so use the FITS stretching as defined in the instrument
        # source.
        return fits_stretch
