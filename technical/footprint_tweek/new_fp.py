__all__ = ("UpdateFootPrint",)

import warnings

import astropy.units as u
import healpy as hp
import numpy as np
from astropy.coordinates import SkyCoord
from rubin_scheduler.scheduler.utils import EuclidOverlapFootprint
from rubin_scheduler.utils import DEFAULT_NSIDE, angular_separation


class UpdateFootPrint(EuclidOverlapFootprint):
    def __init__(
        self,
        nside=DEFAULT_NSIDE,
        dust_limit=0.199,
        smoothing_cutoff=0.45,
        smoothing_beam=10,
        lmc_ra=80.893860,
        lmc_dec=-69.756126,
        lmc_radius=6,
        smc_ra=13.186588,
        smc_dec=-72.828599,
        smc_radius=4,
        scp_dec_max=-60,
        gal_long1=335,
        gal_long2=25,
        gal_lat_width_max=23,
        center_width=12,
        end_width=4,
        gal_dec_max=12,
        low_dust_dec_min=-70,
        low_dust_dec_max=15,
        adjust_halves=12,
        dusty_dec_min=-90,
        dusty_dec_max=15,
        eclat_min=-10,
        eclat_max=10,
        eclip_dec_min=0,
        nes_glon_limit=45.0,
        virgo_ra=186.75,
        virgo_dec=12.717,
        virgo_radius=8.75,
        euclid_contour_file=None,
    ):
        self.nside = nside
        self.hpid = np.arange(0, hp.nside2npix(nside))
        self.read_dustmap()

        self.lmc_ra = lmc_ra
        self.lmc_dec = lmc_dec
        self.lmc_radius = lmc_radius
        self.smc_ra = smc_ra
        self.smc_dec = smc_dec
        self.smc_radius = smc_radius

        self.virgo_ra = virgo_ra
        self.virgo_dec = virgo_dec
        self.virgo_radius = virgo_radius

        self.scp_dec_max = scp_dec_max

        self.gal_long1 = gal_long1
        self.gal_long2 = gal_long2
        self.gal_lat_width_max = gal_lat_width_max
        self.center_width = center_width
        self.end_width = end_width
        self.gal_dec_max = gal_dec_max

        self.low_dust_dec_min = low_dust_dec_min
        self.low_dust_dec_max = low_dust_dec_max
        self.adjust_halves = adjust_halves

        self.dusty_dec_min = dusty_dec_min
        self.dusty_dec_max = dusty_dec_max

        self.eclat_min = eclat_min
        self.eclat_max = eclat_max
        self.eclip_dec_min = eclip_dec_min
        self.nes_glon_limit = nes_glon_limit

        # Ra/dec in degrees and other coordinates
        self.ra, self.dec = hp.pix2ang(nside, self.hpid, lonlat=True)
        self.coord = SkyCoord(ra=self.ra * u.deg, dec=self.dec * u.deg, frame="icrs")
        self.eclip_lat = self.coord.barycentrictrueecliptic.lat.deg
        self.eclip_lon = self.coord.barycentrictrueecliptic.lon.deg
        self.gal_lon = self.coord.galactic.l.deg
        self.gal_lat = self.coord.galactic.b.deg

        # Set the low extinction area
        self.low_dust = np.where((self.dustmap < dust_limit), 1, 0)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=UserWarning)
            self.low_dust = hp.smoothing(self.low_dust, fwhm=np.radians(smoothing_beam))
        self.low_dust = np.where(self.low_dust > smoothing_cutoff, 1, 0)

        self.euclid_contour_file = euclid_contour_file

    def add_bulgy(self, band_ratios, label="bulgy"):
        """Define a bulge region, where the 'bulge' is a series of
        circles set by points defined to match as best as possible the
        map requested by the SMWLV working group on galactic plane coverage.
        Implemented in v3.0.
        Updates self.healmaps and self.pix_labels.

        Parameters
        ----------
        band_ratios : `dict` {`str`: `float`}
            Dictionary of weights per band for the footprint.
        label : `str`, optional
            Label to apply to the resulting footprint
        """
        # Some RA, dec, radius points that
        # seem to cover the areas that are desired
        points = [
            [100.90, 9.55, 3],
            [84.92, -5.71, 3],
            [266.3, -29, 17],
            [279, -13, 10],
            [256, -45, 11],
            [155, -56.5, 6.5],
            [172, -62, 5],
            [190, -65, 5],
            [210, -64, 5],
            [242, -58, 6.5],
            [225, -60, 6.5],
        ]
        for point in points:
            dist = angular_separation(self.ra, self.dec, point[0], point[1])
            # Only change pixels where the label isn't already set.
            indx = np.where((dist < point[2]) & (self.pix_labels == ""))
            self.pix_labels[indx] = label
            for bandname in band_ratios:
                self.healmaps[bandname][indx] = band_ratios[bandname]

    def return_maps(
        self,
        magellenic_clouds_ratios={
            "u": 0.706,
            "g": 0.706,
            "r": 1.194,
            "i": 1.194,
            "z": 0.369,
            "y": 0.369,
        },
        scp_ratios={"u": 0.1, "g": 0.175, "r": 0.1, "i": 0.135, "z": 0.046, "y": 0.047},
        nes_ratios={"g": 0.255, "r": 0.33, "i": 0.33, "z": 0.23},
        dusty_plane_ratios={
            "u": 0.093,
            "g": 0.26,
            "r": 0.26,
            "i": 0.26,
            "z": 0.26,
            "y": 0.093,
        },
        low_dust_ratios={"u": 0.35, "g": 0.4, "r": 1.0, "i": 1.0, "z": 0.9, "y": 0.9},
        bulge_ratios={
            "u": 0.184,
            "g": 1.01,
            "r": 1.062,
            "i": 1.062,
            "z": 1.01,
            "y": 0.223,
        },
        virgo_ratios={"u": 0.35, "g": 0.4, "r": 1.0, "i": 1.0, "z": 0.9, "y": 0.9},
        euclid_ratios={"u": 0.35, "g": 0.4, "r": 1.0, "i": 1.0, "z": 0.9, "y": 0.9},
    ):
        # Array to hold the labels for each pixel
        self.pix_labels = np.zeros(hp.nside2npix(self.nside), dtype="U20")
        self.healmaps = np.zeros(
            hp.nside2npix(self.nside),
            dtype=list(zip(["u", "g", "r", "i", "z", "y"], [float] * 7)),
        )

        # Note, order here matters.
        # Once a HEALpix is set and labled, subsequent add_ methods
        # will not override that pixel.
        self.add_magellanic_clouds(magellenic_clouds_ratios)
        self.add_lowdust_wfd(low_dust_ratios)
        self.add_virgo_cluster(virgo_ratios)
        self.add_bulgy(bulge_ratios)
        self.add_nes(nes_ratios)
        self.add_dusty_plane(dusty_plane_ratios)
        self.add_euclid_overlap(euclid_ratios)
        self.add_scp(scp_ratios)

        return self.healmaps, self.pix_labels
