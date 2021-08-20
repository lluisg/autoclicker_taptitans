# TapTitans Autoclicker

Implementation with Python of an autoclicker for the Taptitans game simulated on BlueStacks 5.0.
It works by having two threads, one that clicks very very quick (200taps/s) and the other that goes around upgrading the mercenaries and the hero every so often. Additionally, some implementation for manual changes: pause, reestart and only press the screen to attack.
It doesn't work perfectly as it depends on the pixel positions, and everytime the game was booted it changed the position by a little margin, enough that it doesn't work as well as it should.