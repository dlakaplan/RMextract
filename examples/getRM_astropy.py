import logging
logging.basicConfig(level=logging.WARNING)

log = logging.getLogger()
import RMextract.getRM as gt
from astropy import units as u, constants as c
from astropy.time import Time
from astropy.coordinates import SkyCoord, EarthLocation



def getRM_astropy(pointing,
                  starttime,
                  stoptime,
                  site,
                  timestep=100*u.s,
                  ionexPath='./IONEXdata/'):
    """Compute RM for a single position/site and a range of times

    Parameters
    ----------
    pointing : `astropy.coordinates.SkyCoord`
    starttime : `astropy.time.Time`
    stopttime : `astropy.time.Time`
    site : `astropy.coordinates.EarthLocation`
    timestep : `astropy.units.Quantity`, optional
    ionexPath : str, optional

    Returns
    -------
    times : `astropy.time.Times`
    RM : `numpy.ndarray`
    """

    RMdict = gt.getRM(ionexPath=ionexPath,
                      radec=[pointing.ra.rad,pointing.dec.rad],
                      timestep=timestep.to_value(u.s),
                      timerange = [(starttime.mjd*u.d).to_value(u.s), (stoptime.mjd*u.d).to_value(u.s)],
                      stat_positions=[[x.value for x in site.to_geocentric()],])
    if RMdict is None:
        log.error("No RM results returned")
        return None,None
    RM = RMdict['RM']['st1']
    times = Time(RMdict['times']/3600/24, format='mjd')
    return times, RM

  
startt = Time('2010-01-01T00:00:00',format='isot',scale ='utc')
endt = startt + 1*u.hr
pointing=SkyCoord(2.15374123*u.rad,  0.8415521*u.rad)
station = EarthLocation.of_site("chime")
#station = EarthLocation.from_geocentric(3826577.1095  ,461022.900196, 5064892.758, unit=u.m)

times,RM = getRM_astropy(pointing, startt, endt, station)
#RM = RMdict['RM']['st1']
#times = Time(RMdict['times']/3600/24, format='mjd')
print ("TIME(mjd)     RM (rad/m^2)")
for tm,rm in zip(times,RM):
    print ("%s        %1.3f"%(tm.iso,rm))
