import numpy as np
import rasterio
from rasterio import transform
from rasterio.warp import reproject, Resampling


def main():
    with rasterio.Env():
        with rasterio.open('netcdf:c_gls_NDVI300_201905210000_GLOBE_PROBAV_V1.0.1.nc:NDVI') as dataset:

            # As source:
            # degrees N, each pixel covering 15".
            rows, cols = src_shape = (47040, 120960)
            d = 1.0 / 336  # decimal degrees per pixel
            # The following is equivalent to
            # A(d, 0, -cols*d/2, 0, -d, rows*d/2).
            west, south, east, north = [-180.0014880952381020,
                                        -59.9985119047300515,
                                        179.9985119063989885,
                                        80.0014880952380878]
            src_transform = transform.from_bounds(west, south, east, north, cols, rows)
            src_crs = {'init': 'EPSG:4326'}
            source = dataset.read()

            # As destination:
            dst_shape = (15680, 40320)
            west, south, east, north = [-180.0044642857142776,
                                        -59.9955357142539043,
                                        179.9955357147768495,
                                        80.0044642857142918]
            dst_transform = transform.from_bounds(west, south, east, north, cols, rows)
            dst_crs = {'init': 'EPSG:4326'}
            destination = np.zeros(dst_shape, np.int16)

            resempling_name = ['average', 'bilinear', 'cubic', 'cubic_spline', 'gauss', 'lanczos']

            for resempling in resempling_name:
                reproject(
                    source,
                    destination,
                    src_transform=src_transform,
                    src_crs=src_crs,
                    dst_transform=dst_transform,
                    dst_crs=dst_crs,
                    resampling=getattr(Resampling, resempling))

                # Assert that the destination is only partly filled.
                assert destination.any()
                assert not destination.all()


if __name__ == '__main__':
    main()