# Greenhouse

## Setup
First, the project is uses the Pico Enviro+ module with the software from the following (link)[https://gitlab.mi.hdm-stuttgart.de/iotee/firmware/-/packages].
To install the firmware, you need to connect your device to your pc while holding down the reset button on the back of case. This will open the file explorer. Now you can upload the firmware (.uf2 file) to the module.

### Device Code Setup
To add the python packages for the project you can run `pip install -r requirements.txt`.
The certificates and com port (when using windows) are saved in a config.py which should be located in the client-folder.
The file should contain the following:

```python 
mqtt_url = 'a3uf1j30lr99lx-ats.iot.eu-central-1.amazonaws.com'
root_ca = ''
public_crt = ''
private_key = ''
COM_port = ''
```

### Terraform Setup
Create a terraform.tfvars file in the terraform directory and insert the following code:
```terraform    
aws_access_key = ""
aws_secret_key = ""
```
and populate the fields with the access and secret key of your AWS account.
Alternatively you can enter your keys in the terminal when running terraform apply.

## Run
To set up the AWS cloud infrastructure you can run the `terraform -chdir=terraform/ init` and `terraform -chdir=terraform/ apply` command.

Now when you run `python ./client/receiver.py` `python ./client/publisher.py`.
The `publisher.py` file reads the sensors of a device and sends the data to the cloud. To debug you can enable the `button_mode` by to pressing the buttons. Now predefined test data instead of sensor data will be sent to the cloud.
The `receiver.py` code uses the data it receives to trigger various actions on a device.