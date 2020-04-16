.. _install:

Installation Guide
==================

Docker
------

The easiest way to use RTC is via docker.

.. code-block:: shell
    
    docker pull rtcproject/rtc:latest

This will create docker image ``rtc:latest``.

.. code-block:: shell
    
    docker run -it rtcproject/rtc:latest

Create and start a container, RTC is out-of-the-box along with miniconda with python3.6.

.. code-block:: python
    
    import rtc
    eng = rtc.Engine

Build From Source
-----------------

If you want to get nightly version of RTC or running on native system, you can build RTC from source. Currently, we only support building on Unix systems. This guide is based on Ubuntu 16.04.

RTC has little dependencies, so building from source is not scary.

1. Check that you have python 3 installed. Other version of python might work, however, we only tested on python with version >= 3.5.


2. Install cpp dependencies

.. code-block:: shell
    
    sudo apt update && sudo apt install -y build-essential cmake

3. Clone RTC project from github.

.. code-block:: shell
    
    git clone https://github.com/rtc-project/RTC.git
    
4. Go to RTC project's root directory and run

.. code-block:: shell
    
    pip install .

5. Wait for installation to complete and RTC should be successfully installed.

.. code-block:: python
    
    import rtc
    eng = rtc.Engine

For Windows Users
------------------

For Windows users, it is recommended to run RTC under Windows Subsystem for Linux (WSL) or use docker.
