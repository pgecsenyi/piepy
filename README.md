# PiEPy

_PiE_ stands for Pi Entertainment. It consists of several modules. _PiEPy_ is a lightweight media server which builds a database from the media files on your machine and allows controlling your server through the local network by publishing a REST API. It is completely privacy aware, does not connect to the internet and will not track you in any way.

## Installation and usage

Python server runs on a Linux operating system (specifically it has been tested on _Ubuntu 16.04_ and on _Raspbian 8_, but it may run on any other recent Linux distribution as well).

First of all make sure you have Python 3 and pip installed along with an appropriate media player (either _VLC_ or _omxplayer_). Also install `pipenv` in case it is not installed already (`pip install --user pipenv`).

Copy the contents of the folder `src` to a location of your choice and navigate to it in the _Terminal_. Then run the following command.

    pipenv update

You can generate a configuration file by executing the server with the `-i` switch.

    pipenv run python main.py -i -c config.cfg

Take a look at the default configuration settings and edit them if you want. When you run the application, you can specify the location of the configuration file from the command line using the `-c` or `--config` arguments. The default location of the configuration file is `config.cfg`.

    pipenv run python main.py -c ../data/config.cfg

Please note the following.

  * In case you are using _omxplayer_, you will need to run the server as the member of the _video_ group.
  * In case you are using _VLC_ or _feh_, will need to run the server as the user who started the X session.
  * In case you are using _fbi_, you will need to run the server from a Linux console (`/dev/ttyN`), a pseudo tty (_xterm_, _ssh_, _screen_, etc.) will not work.
  * _omxplayer_ is the recommended option when the server is running on _Raspberry Pi_, since it is much lighter on resources.
  * If you would like to use port 80, then you will have to run the server as root. Running the application as root is strongly discouraged however.

## Development environment

  * OS
    * Ubuntu 16.04
    * Raspbian GNU/Linux 8 (jessie) raspberrypi 4.9.20-v7+
  * Python
    * Python 3.5.2
    * Python PIP 9.0.1
    * pylint 1.6.5
  * Media players
    * VLC 2.2.2
    * omxplayer build Tue, 10 Feb 2015 01:49:30 +0000
  * Image viewers
    * fbi 2.07, compiled on Dec 29 2013
    * feh 2.9.3 Compile-time switches: curl exif xinerama
    * xdotool 3.20140217.1
