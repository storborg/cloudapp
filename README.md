Cloudapp
========

Install:

    $ pip install cloudapp

Log in:

    $ cat > ~/.cloudapp
    [cloudapp]
    email: alyssa.p.hacker@gmail.com
    password: l!spforl!fe

Upload a file:

    $ cloudapp foo.png

Upload a screenshot of the whole screen:

    $ cloudapp all

Upload a screenshot of a single window:

    $ cloudapp window:gvim

Currently focused on Ubuntu with Unity, but hopefully this will support a range
of platforms soon.
