Welcome to MiTV's documentation!
================================

**MiTV** is a website for hosting the *Mines Saint-Étienne*'s photo association.
It consists of a front-end, back-end and media processor which are supposed to be run in an OpenMediaVault instance via Docker.

The frontend consists of a website to access the drive’s content in a user friendly way.

The backend has a storage API but it also generates useful media metadata.

Features
--------

* Face recognition
* Image similarity detection and grouping
* Image conversion and compression (JPEG)
* Video thumbnailization and compression (AV1)
* Pre-treatment for optimization

Check out the :doc:`usage` section for Installation instructions.

.. note::

   This project is still under development.

Contents
--------

.. toctree::

   usage
   api
