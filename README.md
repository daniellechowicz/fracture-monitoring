# Fracture Monitoring
 A script that analyzes crack length based on frames obtained during a tensile test

## How to set up the software?
1. Go to https://www.python.org/ftp/python/3.7.0/python-3.7.0-amd64.exe

<p align="center"> 
<img src="https://github.com/daniellechowicz/fracture-monitoring/blob/main/assets/setup/1.png">
</p>

2. Install the downloaded file (which is a Python interpreter) and make sure **Add Python 3.7 to PATH** is checked

<p align="center"> 
<img src="https://github.com/daniellechowicz/fracture-monitoring/blob/main/assets/setup/2.png">
</p>

3. When the installation is complete, press **Close**

<p align="center"> 
<img src="https://github.com/daniellechowicz/fracture-monitoring/blob/main/assets/setup/3.png">
</p>

4. Clone or download the content of the repository
5. Extract **hardis-master.zip** and open the folder
6. Open the command prompt in the folder you extracted and execute the following commands, respectively:

```
py -3 -m venv .venv
```
```
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
```
```
.venv\Scripts\activate.ps1
```
or
```
.venv\Scripts\activate
```
8. For the application to work properly, install the required modules:
```
pip install -r requirements.txt
```
9. If the above steps have been correctly performed, the software is ready to use

## How to use the software?
1. Open the command prompt in the folder you extracted and execute the following command to get the instructions:
```
python run.py --help
```
2. The following example illustrates how the software can be used:
```
python run.py -p "your\absolute\folder\path" -ch 2 -fs 100000
```

## Issues related to data acquisition and file format
1. As the modal tests were performed at a sampling rate of 100 000 Hz, the sampling rate of the measurement files must be the same (i.e. 100 000 Hz)
2. The format of the measurement files must be **.txt**
3. Columns must be separated with semicolons
4. Nor headers neither comments are allowed
5. Before running the software, you need to specify channel corresponding to Y axis (remember that the numbering in Python starts with 0)
