# UiO-IR-Reader


* [General](#general-info)
* [Purpose](#purpose)
* [Instalation](#installation)
* [How-to](#how-to)
* [Git Bash](#git-bash)
* [Contact](#Contact)
* [License](#License)


## General

UiO-IR-Reader is a python package to be used for 
changing the format of Bruker OPUS raw data files form Bruker Vertex70 or Vertex80 IR spectoscopy intruments.
Currently UiO-IR-Reader is used at the section for catalysis at
the University of Oslo.

## Purpose

UiO-IR-Reader was created to improve data accecebility of meta data and has been designed
to be easily used. IT utalizes the bruckeropusreader package to more easily handle raw OPUS files.

## Installation

Install the package with pip using the following commands in the command promt in your enviornment. The enviornment need to have `python>=3.9.7` and `pip`
installed.

Git bash and Anaconda Promt:
```
$ git clone  https://github.uio.no/SMN-Catalysis/UiO-IR-Reader
```
```
$ cd Methane-TPR/
```
```
$ pip install .
```

## How-to
To change and convert the raw OPUS-files, the following workflow is to be used.


1. Import DRIFTS, Transmission and ATR clases like:
```
from uio_irreader.reader import DRIFTS, Transmission, ATR
```
2. Define the type of experiment like:
```
object = DRIFTS(directory=r'DIRECTORY OF THE FILE')
```
3. Change data types and quicly visualize like:
```
object.to_KM()
object.wave_number_to_micro_meter()
object.plot()
```
4. Save the changes as a `.csv` or `.xlsx` files like the following:
```
object.to_csv()
object.to_excel()
```

To access the metadata, use the `print(object)`. To get an overview of the differnt function, use the following `object.help()`.


The program keeps track of what changes that have been done, so that only viable changes are possible. To cycle though more than one file at a time, run the script though a `for`-loop for all OPUS-files in a folder.


## Git Bash
The software can also be run in the terminal using `Git Bash`. To install the package, run the folowing in the bash treminal:
1. Download the package using the following command:
```
$ git clone https://github.uio.no/SMN-Catalysis/UiO-IR-Reader.git
```
2. Then move to the newly creater folder with the script:
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
To cycle though more than one file at a time, run the script though a loop for all OPUS-files in a folder.



## Contact

For developer issues, please start a ticket in Github. You can also write to the dev team directly at  **b.g.solemsli@smn.uio.no**
#### Authors: 
Bjørn Gading Solemsli (@bjorngso) & Nicolai Haaber Junge (@nicolhaa).

## License
This script is under the MIT license scheme. 



