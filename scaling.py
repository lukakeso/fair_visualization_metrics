def scaling(data: float, rmin: float, rmax: float, tmin: float, tmax: float) -> float:
    """So let

    rmin: denote the minimum of the range of your measurement
    rmax: denote the maximum of the range of your measurement
    tmin: denote the minimum of the range of your desired target scaling
    tmax: denote the maximum of the range of your desired target scaling
    m ∈ [rmin,rmax]: denote your measurement to be scaled

    Then

    m -> (m - rmin) / (rmax - rmin) * (tmax - tmin) + tmin

    will scale m linearly into [tmin,tmax] as desired.
    """

    
    #
    # To go step by step,
    #
    # m↦m−rmin
    #  maps m
    #  to [0,rmax−rmin]
    # .
    # Next,
    # m↦m−rminrmax−rmin
    # maps m
    #  to the interval [0,1]
    # , with m=rmin
    #  mapped to 0
    #  and m=rmax
    #  mapped to 1
    # .
    #
    # Multiplying this by (tmax−tmin)
    #  maps m
    #  to [0,tmax−tmin]
    # .
    #
    # Finally, adding tmin
    #  shifts everything and maps m
    #  to [tmin,tmax]
    #  as desired.