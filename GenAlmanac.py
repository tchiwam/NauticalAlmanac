#!/usr/bin/python3

import ephem
import datetime
import math
import sys


class degconvert:
    def __init__(self):
        self.reset()
        self.format1 = "%+4d %4.1f"
        self.format2 = "     %4.1f"
    def reset(self):
        self.degree = None
    def rad2degmin(self,x):
        minutes ,degree =  math.modf((x/math.pi) * 180)
        minutes = math.fabs(minutes * 60.0)
        if self.degree == None or self.degree != degree:
            self.degree =  degree
            return str(self.format1 % (degree,minutes))
        else:
            return str(self.format2 % (minutes))

def moonPhase(date):
    mydate  = ephem.date(date.replace(hour=00,minute=0,second=0,microsecond=0))
    nnm   = ephem.next_new_moon(mydate)
    nqm   = ephem.next_first_quarter_moon(mydate)
    nfm   = ephem.next_full_moon(mydate)
    nlm   = ephem.next_last_quarter_moon(mydate)
    quarter = ""
    if nfm>nqm:
        quarter = "Waxing Crescent"
    if nqm>nfm:
        quarter = "Waxing Gibbous"
    if nfm>nlm:
        quarter = "Waning Gibbous"
    if nlm>nnm:
        quarter = "Waning Crescent"
    if nnm.datetime().replace(hour=0,minute=0,second=0,microsecond=0) ==  date.replace(hour=0,minute=0,second=0,microsecond=0):
        quarter = "New %s" % nnm.datetime().strftime("%H:%M:%S")
    if nfm.datetime().replace(hour=0,minute=0,second=0,microsecond=0) ==  date.replace(hour=0,minute=0,second=0,microsecond=0):
        quarter = "Full %s "  % nfm.datetime().strftime("%H:%M:%S")
    if nqm.datetime().replace(hour=0,minute=0,second=0,microsecond=0) ==  date.replace(hour=0,minute=0,second=0,microsecond=0):
        quarter = "First quarter %s " % nqm.datetime().strftime("%H:%M:%S")
    if nlm.datetime().replace(hour=0,minute=0,second=0,microsecond=0) ==  date.replace(hour=0,minute=0,second=0,microsecond=0):
        quarter = "Last quarter %s " % nlm.datetime().strftime("%H:%M:%S")

    return quarter

def seasonPhase(date):
    season = ""
    nss = ephem.next_summer_solstice(date).datetime()
    nae = ephem.next_autumnal_equinox(date).datetime()
    nws = ephem.next_winter_solstice(date).datetime()
    nve = ephem.next_vernal_equinox(date).datetime()
    if nss>nae:
        season = "Summer"    
    if nae>nws:
        season = "Autumn"    
    if nws>nve:
        season = "Winter"    
    if nve>nss:
        season = "Spring"    
    if date == nss.replace(hour=0,minute=0,second=0,microsecond=0):
        season = "Summer Solstice %s" % nss.strftime('%Y.%m.%d %H:%M:%S')
    if date == nae.replace(hour=0,minute=0,second=0,microsecond=0):
        season = "Autumnal equinox %s" % nae.strftime('%Y.%m.%d %H:%M:%S')
    if date == nws.replace(hour=0,minute=0,second=0,microsecond=0):
        season = "Winter solstice %s" % nws.strftime('%Y.%m.%d %H:%M:%S')
    if date == nve.replace(hour=0,minute=0,second=0,microsecond=0):
        season = "Vernal equinox %s" % nve.strftime('%Y.%m.%d %H:%M:%S')
    return season

sunDec=degconvert()
sunDec.format1 = "%+3d %5.2f"
sunDec.format2 = "    %5.2f"
sunRa=degconvert()
Radius=degconvert()
moonDec=degconvert()
moonDec.format1 = "%+3d %5.2f"
moonDec.format2 = "    %5.2f"
moonRa=degconvert()
ariesBDec=degconvert()
ariesBRa=degconvert()


if len(sys.argv) > 1:
    tnow = datetime.datetime.strptime(sys.argv[1],'%Y.%m.%d')
else:
    tnow = datetime.datetime.utcnow()


ttoday = tnow.replace(hour=0,minute=0,second=0,microsecond=0)

print("Date : %s %s" % (tnow.strftime("%Y.%m.%d"),seasonPhase(ttoday) ))
sun    = ephem.Sun()
moon   = ephem.Moon()
ariesB = ephem.readdb('Sheratan,f|S|A5,01:54:38.41099|98.74,28:48:28.9133|-110.41,2.6555,2000,0')
obs    = ephem.Observer()

print("GMT | Sun   GHA       Dec  | Moon  GHA       Dec  |AriesB GHA       ")
for i in range(0,24):
    tcompute = ttoday.replace(hour=i)
    obs.date = tcompute 
    sun.compute(obs)
    sgha = sunRa.rad2degmin((obs.sidereal_time() - sun.g_ra)%(2*math.pi))
    sdec = sunDec.rad2degmin(sun.g_dec)
    moon.compute(obs)
    mgha = moonRa.rad2degmin((obs.sidereal_time() - moon.g_ra)%(2*math.pi))
    mdec = moonDec.rad2degmin(moon.g_dec)
    ariesB.compute(obs)
    ariesBgha = ariesBRa.rad2degmin(obs.sidereal_time()%(2*math.pi))
    print("%02d  | %s %s  | %s %s  | %s" % (i,sgha,sdec,mgha,mdec,ariesBgha)) 
print("")
print("    Sun ----------- Rise --------------          ----------------- Set ------------- | Moon %s" % moonPhase(ttoday))
print("Lat    Astro Nautical    Civil           Transit             Civil Nautical    Astro |     Rise Transit       Set")
tcompute = ttoday.replace(hour=0)
obs.date= tcompute
for i in range(+90,-91,-10):
    obs.lat = (float(i)/360.0)*2*math.pi
    
    obs.horizon = -(18.0/360.0)*2*math.pi
    sun.compute(obs)
    if sun.neverup:
        SunASet  = " Never "
        SunARise = " Never "
    else:
        if sun.circumpolar:
            SunASet  = " Always "
            SunARise = " Always "
        else:
            SunARise = obs.next_rising(ephem.Sun(),use_center=True).datetime().strftime("%H:%M:%S")
            SunASet  = obs.next_setting(ephem.Sun(),use_center=True).datetime().strftime("%H:%M:%S")
    
    obs.horizon = -(12.0/360.0)*2*math.pi
    sun.compute(obs)
    if sun.neverup:
        SunNSet  = " Never "
        SunNRise = " Never "
    else:
        if sun.circumpolar:
            SunNSet  = " Always "
            SunNRise = " Always "
        else:
            SunNRise = obs.next_rising(ephem.Sun(),use_center=True).datetime().strftime("%H:%M:%S")
            SunNSet  = obs.next_setting(ephem.Sun(),use_center=True).datetime().strftime("%H:%M:%S")
    
    obs.horizon = -(6.0/360.0)*2*math.pi
    sun.compute(obs)
    if sun.neverup:
        SunCSet  = " Never "
        SunCRise = " Never "
    else:
        if sun.circumpolar:
            SunCSet  = " Always "
            SunCRise = " Always "
        else:
            SunCRise = obs.next_rising(ephem.Sun(),use_center=True).datetime().strftime("%H:%M:%S")
            SunCSet  = obs.next_setting(ephem.Sun(),use_center=True).datetime().strftime("%H:%M:%S")
    
    obs.horizon = 0
    sun.compute(obs)
    if sun.neverup:
        SunSet  = " Never "
        SunRise = " Never "
    else:
        if sun.circumpolar:
            SunSet  = " Always "
            SunRise = " Always "
        else:
            SunRise = obs.next_rising(ephem.Sun(),use_center=True).datetime().strftime("%H:%M:%S")
            SunSet  = obs.next_setting(ephem.Sun(),use_center=True).datetime().strftime("%H:%M:%S")
    
    if i == 0: 
        SunTransit  = obs.next_transit(sun).datetime().strftime("%H:%M:%S")
    else:
        SunTransit  = " " 
    moon.compute(obs)
    try:
        MoonRise = obs.next_rising(moon,use_center=True).datetime().strftime("%H:%M:%S")
    except:
        MoonRise = "-"
    try:
        MoonSet  = obs.next_setting(moon,use_center=True).datetime().strftime("%H:%M:%S")
    except:
        MoonSet  = "-"
    if i == 0:
        MoonTransit  = obs.next_transit(moon).datetime().strftime("%H:%M:%S")
    else:
        MoonTransit  = " "

    print("%+03d %8s %8s %8s %8s %8s %8s %8s %8s %8s | %8s %8s %8s" % (i,SunARise,SunNRise,SunCRise,SunRise,SunTransit,SunSet,SunCSet,SunNSet,SunASet,MoonRise,MoonTransit,MoonSet))
Radius.format1 = "%+4d %5.2f"
Radius.format2 = "     %5.2f"
Radius.reset()
s0 = "Sun radius: %s" % Radius.rad2degmin(sun.radius)
Radius.reset()
s1 = "Moon radius: %s" % Radius.rad2degmin(moon.radius)
print ("%s                                                               | %s" % (s0,s1))
