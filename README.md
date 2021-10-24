# rat-solar-modelling

Modelling production characteristics of a temporary 1-week solar generator in the Nevada desert.  

# Getting Started

Install dependencies using [poetry](https://python-poetry.org):

```shell
poetry install
```

If using pycharm, the [poetry plugin](https://plugins.jetbrains.com/plugin/14307-poetry) helps setting up the python
interpretter to use the poetry virtualenv.

Then fire up the jupyter notebook server from a virtualenv shell. The `bin/jupyter.sh` script helps configure paths 
for you:

```shell
poetry shell
./bin/jupyter.sh
```

# PVWatts API

You need to get a PVWatts API key to run these scripts. Get one at [https://developer.nrel.gov/docs/solar/pvwatts/](https://developer.nrel.gov/docs/solar/pvwatts/)
and then set it as your `PVWATTS_API_KEY` envvar.
