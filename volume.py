#!/usr/bin/env python3


from __future__ import division
import glob
import powermate
import alsaaudio


class VolPowerMate(powermate.PowerMateBase):

    def __init__(self, path, alsa_mixer=None):
        super(VolPowerMate, self).__init__(path)
        self._m = self.getmixer(alsa_mixer)

    def getmixer(self, alsa_mixer):
        if alsa_mixer:
            return alsaaudio.Mixer(alsa_mixer)
        else:
            return alsaaudio.Mixer()

    def getvolume(self):
        left, right = self._m.getvolume()
        return (left + right) / 2

    def getmute(self):
        left, right = self._m.getmute()
        return left or right

    def setvolume(self, vol):
        self._m.setvolume(vol)

    def setmute(self, mute):
        self._m.setmute(mute)

    def rotate(self, rotation):
        if not self.getmute():
            vol = min(100, max(0, self.getvolume() + rotation))
            self.setvolume(int(vol))
            return powermate.LedEvent.percent(vol / 100)
        else:
            return powermate.LedEvent.pulse()

    def short_press(self):
        if self.getmute():
            self.setmute(0)
            return powermate.LedEvent.percent(self.getvolume() / 100)
        else:
            self.setmute(1)
            return powermate.LedEvent.pulse()


def main():
    """
    Main function for checking input device existance and initialization.
    """
    mixer = 'Headphone'

    pm_devices = glob.glob('/dev/input/by-id/*PowerMate*')
    if not pm_devices:
        return

    pm_device = pm_devices[0]
    VolPowerMate(pm_device, mixer).run()


if __name__ == '__main__':
    main()
