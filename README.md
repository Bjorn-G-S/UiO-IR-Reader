# UiO-IR-Reader


* [General](#general-info)
* [Purpose](#purpose)
* [Instalation](#installation)
* [How-to](#how-to)
* [Comments](#Comments)


## General

UiO-IR-Reader is a python package to be used for 
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

Download the  python script and open in Jupyter lab or your program of choise. Spesify what type of IR experiment have been used by choosing the right program (`obj = DRIFTS(r'file directory')` or `obj = Transmission(r'file directory)`).

To access the metadata, use the `print(obj)`. To get an overview of the differnt function, use the following `obj.help()`.


The program keeps track of what changes have been doe so that only viable changed is possible. To cycle though more than one file at a time, run the script though a for loop for all OPUS-files in a directory.


### Git Bash
The software can also be run in the terminal using `Git Bash`. To install the package, run the folowing in the bash treminal:


`$ git clone https://github.uio.no/SMN-Catalysis/UiO-IR-Reader.git`
 

`$ cd UiO-IR-Reader/`
 

`$ pip install .`
 

`$ uio_irreader -h`




## Comments


For any questions please email **b.g.solemsli@smn.uio.no**



