Piezosystem Jena NV40/3CLE
##########################

.. image:: https://img.shields.io/pypi/v/pymodaq_plugins.svg
   :target: https://pypi.org/project/pymodaq_plugins/
   :alt: Latest Version

.. image:: https://readthedocs.org/projects/pymodaq/badge/?version=latest
   :target: https://pymodaq.readthedocs.io/en/stable/?badge=latest
   :alt: Documentation Status

.. image:: https://github.com/CEMES-CNRS/pymodaq_plugins/workflows/Upload%20Python%20Package/badge.svg
    :target: https://github.com/CEMES-CNRS/pymodaq_plugins

PyMoDAQ plugin for controlling PiezosystemJena voltage amplifier NV40/3 CLE.
This amplifier is well suited for sub-nm positioning tasks.

The plugin does provide limited support for single-axis (NV40/1CLE) and open-loop controller of the same series
as it was not a target application at the time of writing the plugin.

The control library relies on the pyserial module to communicate with the device using Serial process over usb.

Installing the manufacturer's driver for USB interface is required (Driver USB Software in the following link):
https://www.piezosystem.com/about-navigation/downloads/

Authors
=======
* Nicolas Tappy

Instruments
===========
Below is the list of instruments included in this plugin

Actuators
+++++++++
* NV40/3CLE: Closed loop voltage amplifier for the control of piezo elements.
