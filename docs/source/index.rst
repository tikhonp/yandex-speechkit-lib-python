.. speechkit documentation master file, created by
   sphinx-quickstart on Tue Jul 20 03:54:03 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to speechkit's documentation!
=====================================

Speechkit is python SDK for Yandex SpeechKit API.

Installation
-----------

Assuming that you have Python and virtualenv installed, set up your environment and install the required dependencies
like this::


   $ git clone https://github.com/TikhonP/yandex-speechkit-lib-python.git
   $ cd yandex-speechkit-lib-python
   $ virtualenv venv
   ...
   $ . venv/bin/activate
   $ python -m pip install -r requirements.txt
   $ python -m pip install .

Or you can install the library using pip::

   python -m pip install speechkit
   
Api Reference
-----------

.. toctree::
   :maxdepth: 2
   :caption: Contents:
    
   speechkit

   auth

   utils

   exceptions


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
