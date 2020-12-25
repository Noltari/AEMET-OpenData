AEMET-OpenData is a Python module implementing an interface to the AEMET OpenData Rest API.  
It allows a user to gather all the public weather information from AEMET (Agencia Estatal de Meteorología).

Documentation for the AEMET OpenData Rest API is available at https://opendata.aemet.es/.

This package has been developed to be used with https://home-assistant.io/ but it can be used in other contexts.

Disclaimer
----------

AEMET-OpenData was created for my own use, and for others who may wish to experiment with personal Internet of Things systems.

I have no connection with AEMET. I receive no help (financial or otherwise) from AEMET, and have no business interest with them.

This software is provided without warranty, according to the GNU Public Licence version 2, and should therefore not be used where it may endanger life, financial stakes, or cause discomfort and inconvenience to others.

Usage
-----

```
from aemet_opendata.interface import AEMET
_aemet = AEMET(api_key="my_api_key")
town = _aemet.get_town(municipio="id28065")
```
