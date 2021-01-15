# Fracture Monitoring
A script that analyzes crack length and its rotation based on frames obtained during a tensile test of standard samples
<p align="center"> 
<img src="https://github.com/daniellechowicz/fracture-monitoring/blob/main/assets/workpieceGeometry.png">
</p>

<p align="center"> 
<img src="https://github.com/daniellechowicz/fracture-monitoring/blob/main/assets/screenshots/7.png">
</p>

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
5. Extract **fracture-monitoring-master.zip** and open the folder
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
1. Open the command prompt in the folder you extracted and execute the following command to run the application:
```
python app.py
```
2. Then, the following window should pop up:

<p align="center"> 
<img src="https://github.com/daniellechowicz/fracture-monitoring/blob/main/assets/screenshots/1.png">
</p>
