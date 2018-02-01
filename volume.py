#!/usr/bin/env python3

from __future__ import division

import glob, powermate, alsaaudio


class VolPowerMate(powermate.PowerMateBase):
    def __init__(self, path):
        super(VolPowerMate, self).__init__(path)
        self.__m = alsaaudio.Mixer()
        self.__globvol = 25
        self.__m.setvolume(self.__globvol)
        self.__mute = False

    def rotate(self, rotation):
        vol = int(self.__m.getvolume()[0])
        if not self.__mute:
            self.__globvol = min(100, max(0, vol + rotation))
            self.__m.setvolume(self.__globvol)
            return powermate.LedEvent.percent(self.__globvol / 100)
        else:
            return powermate.LedEvent.pulse()

    def short_press(self):
        self.__mute = not self.__mute
        if self.__mute:
            self.__m.setvolume(0)
            return powermate.LedEvent.pulse()
        else:
            self.__m.setvolume(self.__globvol)
            return powermate.LedEvent.percent(self.globvol / 100)


if __name__ == '__main__':
    pm = VolPowerMate(glob.glob('/dev/input/by-id/*PowerMate*')[0])
    pm.run()

