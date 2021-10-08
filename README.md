# UiO-IR-Reader


* [General](#general-info)
* [Purpose](#purpose)
* [Instalation](#installation)
* [How-to](#how-to)
* [Comments](#Comments)


## General

UiO-IR-Reader is a python script to be used for 
changing the format of Bruker OPUS raw data files form Bruker Vertex70 or Vertex80 IR spectoscopy intruments.
Currently UiO-IR-Reader is used at the section for catalysis at
the University of Oslo.

## Purpose

UiO-IR-Reader was created to improve data accecebility of meta data and has been designed
to be easily used. 

## Installation


The following python packages are needed:

<ul>
    <li>python (>= 3.8.8)
    <li>matplotlib (>= 3.3.1)
    <li>pandas (>= 1.2.3)
    <li>numpy (>= 1.19.1)
    <li>brukeropusread (>= 1.3.4)
  
</ul>




## How-to

Download the  python script and open in Jupyter lab or your program of choise. Spesify what type of IR experiment have been used by choosing the right program (`obj = DRIFTS(r'file directory')`, `obj = Transmission(r'file directory)` or `obj = ATR(r'file directory')`).

To access the metadata, use the `print(obj)`. To get an overview of the differnt function, use the following `obj.help()`.




## Comments


For any questions please email **b.g.solemsli@smn.uio.no**



