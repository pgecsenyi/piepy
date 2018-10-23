# PiEPy

_PiE_ stands for Pi Entertainment. It consists of several modules. _PiEPy_ is a lightweight media server which builds a database from the media files on your machine and allows controlling your server through the local network by publishing a REST API. It is completely privacy aware, does not connect to the internet and will not track you in any way.

## Installation and usage

Python server runs on a Linux operating system (specifically it has been tested on _Ubuntu 17.10_ and on _Raspbian 8_, but it may run on any other recent Linux distribution as well).

First of all make sure you have Python 3 and pip installed along with an appropriate media player (either _VLC_ or _omxplayer_). Also install `pipenv` in case it is not installed already (`pip install --user pipenv`). You may have multiple Python environments installed, in this case do not forget to replace `pip` with `pip3` and `python` with `python3` (or whatever the binaries are named on your machine) in the commands listed here.

Copy the contents of the folder `src` to a location of your choice and navigate to it in the _Terminal_. Then run the following command.

    python -m pipenv install

You can generate a configuration file by executing the server with the `-i` switch.

    python -m pipenv run python main.py -i -c config.json

Take a look at the default configuration settings and edit them if you want. When you run the application, you can specify the location of the configuration file from the command line using the `-c` or `--config` arguments. The default location of the configuration file is `config.json`.

    python -m pipenv run python main.py -c ../data/config.json

Please note the following.

  * In case you are using _omxplayer_, you will need to run the server as the member of the _video_ group.
  * In case you are using _VLC_ or _feh_, will need to run the server as the user who started the X session.
  * In case you are using _fbi_, you will need to run the server from a Linux console (`/dev/ttyN`), a pseudo tty (_xterm_, _ssh_, _screen_, etc.) will not work.
  * _omxplayer_ is the recommended option when the server is running on _Raspberry Pi_, since it is much lighter on resources.
  * If you would like to use port 80, then you will have to run the server as root. Running the application as root is strongly discouraged however.

## Development

Install developer dependencies first by running the following command.

    pipenv install --dev

There is a script called `run.sh` in the `src` folder. It accepts 2 parameters. The first parameter can have one of the following values.

  * `clean`: removes Python bytecode files and the directory containing test data from the source folder.
  * `lint`: runs pylint and generates output in the data folder provided as the second parameter.
  * `test`: executes tests and generates output in the data folder provided as the second parameter.
  * `start`: starts the application in debug mode loading the config file from the data folder provided as the second parameter.

The second parameter tells the script where to store output files or load input from. It's default value is `../data`.

_Visual Studio Code_ can be used to debug the application, in order to do that you will first need to configure the path of the Python interpreter in `.vscode/settings.json`.

### Environment

  * OS
    * Ubuntu 17.10
    * Raspbian GNU/Linux 8 (jessie) raspberrypi 4.9.57-v7+
  * Python
    * Python 3.6.3
    * Python PIP 9.0.1
  * Media players
    * VLC 2.2.6
    * omxplayer 05 Jul 2017 17:40:39 UTC 5a25a57
  * Image viewers
    * fbi 2.09
    * feh 2.19 Compile-time switches: curl exif xinerama
    * xdotool 3.20160805.1
  * Code editor
    * Visual Studio Code 1.25.1
      * Extension: Python 2018.7.1
