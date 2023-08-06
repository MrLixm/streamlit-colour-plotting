# streamlit_colourplotting

A streamlit web-application allowing to plot colors on a CIE Diagram using
the [colour-science](https://www.colour-science.org/) library.

![screenshot of the web-app](doc/img/cover.png)

The application allow to plot a single R-G-B color or a whole image using various
methods. A lot of options allow you to customize how the final diagram looks.

# Development

## Getting Started

Assuming you have :

- set the current working directory as desired
- installed [poetry](https://python-poetry.org/) on your system

```shell
git clone https://github.com/MrLixm/streamlit-colour-plotting.git
cd streamlit-colour-plotting
poetry update
```

You should now be able to run the application using the launcher :

```shell
./dev/run-streamlit.sh
```

You can now start editing code in [streamlit_colourplotting/](streamlit_colourplotting).

It is recommended to put in place a file watcher or a pre-commit hook that 
would run [black](https://black.readthedocs.io/en/stable/) on all the files.

## Configuration

### Environment Variables

To use for local development (not on cloud).

- `STCP_DISABLE_SIZE_LIMITATIONS` : to set with any non-empty value. 
    Remove the 2048 size limitation for images upload.
- `APP_LOG_LEVEL` : set the python application logger level. Except a python log level in upper case. ex: `WARNING`

## Logic

Streamlit use a single file as entry point that is re-run everytime a widget
change on the web GUI.

This file is located in [./src/app.py](./src/app.py). It is quite empty and 
only import the python package `streamlit_colourplotting` which define everything.

A important concept to understand :
- streamlit re-run `app.py` from top to bottom everytime
- but python cache imported package on their first import

This mean that anything in the global scope will be shared along users. This why
the "config" system store everything in session_state instead of python global variables.


## Cocoon

Note that for color manipulation, this application use [cocoon](https://github.com/MrLixm/cocoon) which
is mostly a convenient wrapper around colour library.

## Profiling

As streamlit cloud machine are limited in ressources, it's a good idea to 
check the memory profile of our app.

Once the streamlit app is started you can run the
[profile-running-streamlit.sh](dev/profile-running-streamlit.sh) script and
follow its intrsuction (make sure to launch it with the current directory being the 
root of this repo).