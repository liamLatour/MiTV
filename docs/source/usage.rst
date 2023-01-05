Usage
=====

.. _installation:

Installation
------------

Manual install
++++++++++++++

**You must have a mongo database running on the machine**

Start by cloning the repository

.. code:: bash

     git clone https://github.com/liamLatour/MiTV.git
     cd MiTV

Install MiTV frontend with npm

.. code:: bash

     cd mi_tv_frontend
     npm i

Install MiTV backend with Python and install the metadata module

.. code:: bash

     cd mi_tv_backend
     pip install -r requirements.txt
     pip install ./image_metadata

To deploy the frontend, first build it:

.. code:: bash

     npm run build

To deploy the backend run:

.. code:: bash

     waitress-serve --host 127.0.0.1 --port=5000 api_server:app

To run the media processor:

.. code:: bash

     meta_data_creation --prerun --continuous --immediate ./people_ref ./photos

.. warning::

   If you are on Linux and do not use a virtual environment, make sure to add *$USER/.local/bin* to your **PATH**

Docker install
++++++++++++++

Start by cloning the repository

.. code:: bash

     git clone https://github.com/liamLatour/MiTV.git
     cd MiTV

Install MiTV and run the containers

.. code:: bash

     docker compose up

Using the website
-----------------

The default credentials are:

* Username: *admin*
* Password: *pass*