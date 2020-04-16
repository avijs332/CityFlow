# Converter

`converter.py` can convert sumo roadnet files to its corresponding RTC version. 

The following code converts a sumo roadnet file, atlanta.net.xml, to RTC format.

*Example roadnet and flow files can be downloaded [here](https://github.com/rtc-project/data/tree/master/tools/Converter/examples)*

```
python converter.py --sumonet atlanta_sumo.net.xml --rtcnet atlanta_rtc.json
```

SUMO roadnet and transformed RTC roadnet

<p float="left">
    <img src="https://github.com/rtc-project/data/raw/master/tools/Converter/figures/sumo.png" alt="SUMO" height="300px"/>
    <img src="https://github.com/rtc-project/data/raw/master/tools/Converter/figures/city_flow.png" alt="RTC" height="300px" style="margin-left:50px"/>
</p>



#### Dependencies

**sumo** is required and make sure that the environment variable *SUMO_HOME* is set properly. If you have an installation via *apt-get*, you can use `/usr/share/sumo` as the value.

**sympy** is required.  You can install it using pip.