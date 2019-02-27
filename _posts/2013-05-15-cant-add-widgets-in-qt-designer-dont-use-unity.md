Can\'t add widgets in Qt Designer? Don\'t use Unity
===================================================

I got around a problem in Qt designer that didn\'t allow me to drop any
widget. When I tried, I obtained the barred circle mouse pointer,
instead of the plus. When dropped, the drop operation did not complete,
and the receiving widget remained empty. Apparently, it\'s due to some
form of collision between designer and Unity (the graphic environment on
Ubuntu). I switched to Gnome and now designer works. Note that I got it
to work occasionally on Unity as well, but I was never able to reproduce
the exact conditions that allowed it.
