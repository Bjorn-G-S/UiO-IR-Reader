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
to be easily used. IT utalizes the bruckeropusreader package to more easily handle raw OPUS files.

## Installation


The following python packages are needed:

<ul>
    <li>python (>= 3.8.8)
    <li>matplotlib (>= 3.3.1)
    <li>pandas (>= 1.2.3)
    <li>numpy (>= 1.19.1)
    <li>brukeropusreader (>= 1.3.4)
  
</ul>




## How-to
To change and convert the raw OPUS-files, the following workflow is to be used.

1. Install the package in Anaconda Prompt using the following command:
```
(env) C:\>pip install git+http://github.uio.no/SMN-Catalysis/UiO-IR-Reader.git
```
2. Import DRIFTS, Transmission and ATR clases like:
```
from uio_irreader import DRIFTS, Transmission, ATR
```
3. Define the type of experiment like:
```
object = DRIFTS(r'DIRECTORY OF THE FILE')
```
4. Change data types and quicly visualize like:
```
object.R_lgR()
object.plot()
```
5. Save the changes as a `.csv`- or `.xlsx` files like the following:
```
object.to_csv()
object.to_excel()
```



To access the metadata, use the `print(object)`. To get an overview of the differnt function, use the following `object.help()`.


The program keeps track of what changes have been doe so that only viable changed is possible. To cycle though more than one file at a time, run the script though a for loop for all OPUS-files in a directory.


### Git Bash
The software can also be run in the terminal using `Git Bash`. To install the package, run the folowing in the bash treminal:
1. Download the package like:
```
$ git clone https://github.uio.no/SMN-Catalysis/UiO-IR-Reader.git
```
2. Then:
```
$ cd UiO-IR-Reader/
```
3. Install using the following command:
```
$ pip install .
```
4. Run the following to use the program: 
```
$ uio_irreader -h
```




## Comments


For any questions please email **b.g.solemsli@smn.uio.no**



