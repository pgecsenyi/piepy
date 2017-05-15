# PiEPy: Architecture

    +------------------------------------------------+
    |                     Test                       |
    +------------------------------------------------+
    |                     Web                        |
    +------------------------------------------------+
    |            Business Logic Layer                |
    +---------------------+-----------+--------------+
    |  Data Access Layer  |  Indexer  |  Multimedia  |
    +---------------------+-----------+--------------+

The server consists of several more or less independent modules which are structured into layers. At the lowest level there are three, completely independent modules.

  * The _Multimedia_ module is responsible for communicating with multimedia players and viewers.
  * The _Indexer_ module is able to iterate through the contents of a directory and mine interesting data.
  * The _Data Access Layer_ is responsible for persisting and recalling data.

On the top of that, there is the _Business Logic Layer_ which coordinates these three modules. The _Web_ module provides the REST API and there is also a _Test_ module, which contains the unit tests and integration tests.
