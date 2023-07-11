# Greenhouse

## Setup
First, the project is using the Pico Enviro+ module with the software from the following [link](https://gitlab.mi.hdm-stuttgart.de/iotee/firmware/-/packages).
To install the firmware, you need to connect your device to your pc while holding down the reset button on the back of case. This will open the file explorer. Now you can upload the firmware (.uf2 file) to the module.

### Device Code Setup
To add the python packages for the project you can run `pip install -r ./client/requirements.txt`.

### Terraform Setup
Create a terraform.tfvars file in the terraform directory and insert the following code:
```terraform    
aws_access_key = ""
aws_secret_key = ""
```
and populate the fields with the access and secret key of your AWS account.
Alternatively you can enter your keys in the terminal when running terraform apply.

## Run
To set up the AWS cloud infrastructure you can run 
```bash
terraform -chdir=terraform/ init
terraform -chdir=terraform/ apply
```
This will create the necessary resources in AWS and add the certificates for the MQTT connection.

Now when you run 
```bash
python ./client/receiver.py
python ./client/publisher.py
```
The `publisher.py` file will read the sensors of a device and sends the data to the cloud. To debug you can enable the `button_mode` by to pressing the buttons. Now predefined test data instead of sensor data will be sent to the cloud.
The `receiver.py` code uses the data it receives to trigger various actions on a device.