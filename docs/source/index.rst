.. speechkit documentation master file, created by
   sphinx-quickstart on Tue Jul 20 03:54:03 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to speechkit's documentation!
=====================================

Speechkit is python SDK for Yandex SpeechKit API.

Installation
------------

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
-------------

.. toctree::
   :maxdepth: 2
   :caption: Contents:
    
   speechkit

   auth

   utils

   exceptions

Some Shortcuts dor YC console tool
----------------------------------

Get FOLDER_ID: FOLDER_ID=$(yc config get folder-id)

Create service-account: yc iam service-account create --name admin

Get id of service-account: SA_ID=$(yc iam service-account get --name admin --format json | jq .id -r)

Assign a role to the admin service account using its ID: yc resource-manager folder add-access-binding --id $FOLDER_ID --role admin --subject serviceAccount:$SA_ID

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
