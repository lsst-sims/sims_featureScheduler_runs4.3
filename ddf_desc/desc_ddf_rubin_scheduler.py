import numpy as np
from ddf_presched_desc import generate_ddf_scheduled_obs
import pandas as pd
from optparse import OptionParser


def ddf_config(sequence_time=60.0,
               season_unobs_frac=0.2,
               low_season_frac=0,
               low_season_rate=0.3,
               g_depth_limit=23.5,
               field_list=['COSMOS', 'XMM_LSS', 'ELAISS1', 'ECDFS', 'EDFS_a'],
               survey=pd.DataFrame()):
    """
    Function to define the ddf configuration for the rubin scheduler

    Parameters
    ----------
    sequence_time : float, optional
        Expected time for each DDF sequence, used to avoid hitting the
        sun_limit (running DDF visits into twilight). In minutes. 
        The default is 60.0.
    season_unobs_frac : float, optional
        Defines the end of the range of the prescheduled observing season.
        season runs from 0 (sun's apparent position is at the RA of the DDF)
        to 1 (sun returns to an apparent position in the RA of the DDF).
       The scheduled season runs from:
       season_unobs_frac < season < (1-season_unobs_fract)
       The default is 0.2.
    low_season_frac : float, optional
        Defines the end of the range of the "low cadence" prescheduled
        observing season.
        The "standard cadence" season runs from:
        low_season_frac < season < (1 - low_season_frac)
        For an 'accordian' style DDF with fewer observations near
        the ends of the season, set this to a value larger than
        `season_unobs_frac`. Values smaller than `season_unobs_frac`
        will result in DDFs with a constant rate throughout the season.
        The default is 0.
    low_season_rate : float, optional
        Defines the rate to use within the low cadence portion
        of the season. During the standard season, the 'rate' is 1.
        This is used in `ddf_slopes` to define the desired number of
        cumulative observations for each DDF over time.
        The default is 0.3.
    g_depth_limit : float, optional
        The minimum g band five sigma depth limit allowed when prescheduling
        DDF visits. This is a depth limit in g band (mags).
        The depth is calculated using skybrightness from skybrightness_pre,
        a nominal FWHM_500 seeing at zenith of 0.7" (resulting in airmass
        dependent seeing) and exposure time.
        Default 23.5. Set to None for no limit.
        The default is 23.5.
    field_list: list(str)
        List of fields to consider. The default is
        ['COSMOS', 'XMM_LSS', 'ELAISS1', 'ECDFS', 'EDFS_a']
    survey: pandas df
        survey configuration (fields, visits, season_length, sequence_sec)

    Returns
    -------
    ddf_kwargs : dict
        DDF parameters.

    """

    ddf_kwargs = {}

    for field in field_list:
        ddf_kwargs.update(field_dict(field, survey,
                                     sequence_time=sequence_time,
                                     season_unobs_frac=season_unobs_frac,
                                     low_season_frac=low_season_frac,
                                     low_season_rate=low_season_rate,
                                     g_depth_limit=g_depth_limit))

    return ddf_kwargs


def field_dict(field, survey, sequence_time=60.0,
               season_unobs_frac=0.2,
               low_season_frac=0,
               low_season_rate=0.3,
               g_depth_limit=23.5,):
    """
    Make a dict of field parameters

    Parameters
    ----------
    field : str
        field name.
    survey : pandas df
        survey parameters.
    sequence_time : float, optional
        Expected time for each DDF sequence, used to avoid hitting the
        sun_limit (running DDF visits into twilight). In minutes. 
        The default is 60.0.
    season_unobs_frac : float, optional
        Defines the end of the range of the prescheduled observing season.
        season runs from 0 (sun's apparent position is at the RA of the DDF)
        to 1 (sun returns to an apparent position in the RA of the DDF).
       The scheduled season runs from:
       season_unobs_frac < season < (1-season_unobs_fract)
       The default is 0.2.
    low_season_frac : float, optional
        Defines the end of the range of the "low cadence" prescheduled
        observing season.
        The "standard cadence" season runs from:
        low_season_frac < season < (1 - low_season_frac)
        For an 'accordian' style DDF with fewer observations near
        the ends of the season, set this to a value larger than
        `season_unobs_frac`. Values smaller than `season_unobs_frac`
        will result in DDFs with a constant rate throughout the season.
        The default is 0.
    low_season_rate : float, optional
        Defines the rate to use within the low cadence portion
        of the season. During the standard season, the 'rate' is 1.
        This is used in `ddf_slopes` to define the desired number of
        cumulative observations for each DDF over time.
        The default is 0.3.
    g_depth_limit : float, optional
        The minimum g band five sigma depth limit allowed when prescheduling
        DDF visits. This is a depth limit in g band (mags).
        The depth is calculated using skybrightness from skybrightness_pre,
        a nominal FWHM_500 seeing at zenith of 0.7" (resulting in airmass
        dependent seeing) and exposure time.
        Default 23.5. Set to None for no limit.
        The default is 23.5.


    Returns
    -------
    out_dict : dict
        field survey parameters.

    """

    out_dict = {}

    out_dict[field] = {
        "season_seq": get_val_field(survey, field, "season_seq"),
        "boost_early_factor": None,
        "boost_factor_third": 0,
        "g_depth_limit": g_depth_limit,
        "season_unobs_frac": season_unobs_frac,
        "sequence_time": sequence_time,
        "low_season_frac": low_season_frac,
        "low_season_rate": low_season_rate,
        "u": get_val_field(survey, field, "u"),
        "g": get_val_field(survey, field, "g"),
        "r": get_val_field(survey, field, "r"),
        "i": get_val_field(survey, field, "i"),
        "z": get_val_field(survey, field, "z"),
        "y": get_val_field(survey, field, "y"),
        "season_length": get_val_field(survey, field, "season_length")
    }

    return out_dict


def get_val_field(df, field, colName):
    """
    to grab a field survey value

    Parameters
    ----------
    df : numpy array
        Survey parameters.
    field : str
        DDF field name.
    colName : str
        column name.

    Returns
    -------
    list
        values corresponding to colName for the field.

    """

    return df[df['field'] == field][colName].tolist()


def generate_ddf_observations(survey_file="ddf_desc_0.70_sn.npy"):
    ddf_survey = np.load(survey_file, allow_pickle=True)

    # grab ddf configuration for rubin survey
    ddf_kwargs = ddf_config(survey=ddf_survey)
    observations = generate_ddf_scheduled_obs(dist_tol=1,
                                              ddf_kwargs=ddf_kwargs)

    return observations


if __name__ == "__main__":

    parser = OptionParser(
        description='Script to produce DDF observations for the LSST scheduler')

    parser.add_option('--inputDir', type=str,
                      default='./',
                      help='Location dir of input files [%default]')
    parser.add_option('--survey', type=str,
                      default='ddf_desc_0.70_sn.npy',
                      help='config file for visits [%default]')

    opts, args = parser.parse_args()

    inputDir = opts.inputDir
    survey = opts.survey

    # load the survey

    ddf_survey = np.load(f'{inputDir}/{survey}', allow_pickle=True)

    # grab ddf configuration for rubin survey
    ddf_kwargs = ddf_config(survey=ddf_survey)


    # generate observations

    observations = generate_ddf_scheduled_obs(dist_tol=1,
                                              ddf_kwargs=ddf_kwargs)

    print('done', len(observations))
