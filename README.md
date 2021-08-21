# Yantrakaar_Client
GUI client for Yantrakar's local and cloud processing

## Installation Instructions
1. Dependencies (given above)
   - WxPython
   - Mxnet
   - Gluoncv
   - Opencv Contrib Modules
   - Matplotlib
2. Run make_file.py to get the models
3. Make a "FRAMES" folder if already not present
4. Run Main.py

Install wxPython using:
```sh
pip install wxPython
```
or 
```sh
pip install wxwidgets
```

Run these commands to install the rest of the dependencies:
```sh
pip install --user mxnet
pip install gluoncv mxnet-mkl>=1.4.0 --upgrade
pip install opencv-contrib-python
pip install matplotlib
```
