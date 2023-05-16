# Greenhouse

## setup
    
First of all you need to have the correct hardware with the newest software. If the program does not list 4 Sensor datas when running you need to update it. To do so go (here)[https://gitlab.mi.hdm-stuttgart.de/iotee/firmware/-/packages] and download the .uf2 file from the newest version. Connect the sensor device while holding down the reset button on the back. This opens a windows explorer window in which you insert the .uf2 file. __Done__

Then run the comman `pip install -r requirements.txt` to install all the needed python packages.

create a config.py file in the root directory and insert the following code:
```python 
mqtt_url = 'a3uf1j30lr99lx-ats.iot.eu-central-1.amazonaws.com'
root_ca = ''
public_crt = ''
private_key = ''
COM_port = ''
```
and insert all the needed certifications. They can be found in the AWS IoT Core, on the thing. 

After connecting the device figure out which COM Port it's connected to and insert it in the config.py file. To figure that out you can open the device manager and look for USB connections.

## run
