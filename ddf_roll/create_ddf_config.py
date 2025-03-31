import numpy as np
import copy


if __name__ == "__main__":

    # generate a new config

    start = np.load("../ddf_desc_full/ddf_desc_0.75_sn.npy", allow_pickle=True)

    xmm_last = start[np.where(start["field"] == "XMM_LSS")[0][-1]]
    xmm_high = start[np.where(start["field"] == "XMM_LSS")[0][2]]

    end = copy.copy(start)

    indx = np.where((start["field"] == "XMM_LSS") & (start["season"] == 2))
    end[indx] = xmm_last
    end["season"][indx] = 2

    indx = np.where((start["field"] == "ECDFS") & (start["season"] == 2))
    end[indx] = xmm_high
    end["field"][indx] = "ECDFS"
    end["season"][indx] = 2

    indx = np.where((start["field"] == "XMM_LSS") & (start["season"] == 3))
    end[indx] = xmm_last
    end["season"][indx] = 3

    indx = np.where((start["field"] == "ELAISS1") & (start["season"] == 3))
    end[indx] = xmm_high
    end["field"][indx] = "ELAISS1"
    end["season"][indx] = 3

    np.save("ddf_roll_1.npy", end)
