# Greenhouse

This is a proof of concept for an IoT-based greenhouse management system using cloud services technologies.

The project utilizes IoT sensors to gather real-time data parameters such as temperature, humidity and light intensity. This data is then transmitted to a cloud platform, where it is monitored and processed.

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

# Terraform State Management with GitLab
We utilize GitLab's Terraform state backend to manage and store the state of our infrastructure. Follow the instuctions that can be read [here](https://docs.gitlab.com/ee/user/infrastructure/iac/terraform_state.html) To use the GitLab Terraform state backend, it requires the use of a GitLab Personal Access Token. 

You can create a token by following the instructions [here](https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html#creating-a-personal-access-token). The token needs to have the `api` scope.

Once you have your Personal Access Token, you're ready to initialize your Terraform configuration with the GitLab backend. You can find and copy the init command from the GitLab repository Terraform state page under Infrastructure > Terraform states.

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

The `publisher.py` file will read the sensors of a device and sends the data to the cloud. To enter the debug mode you can change the `button_mode` value to True. Now it is possible to send predefined test data instead of sensor data by pressing the iotee buttons to the cloud.
The `receiver.py` code uses the data it receives to trigger various actions on a device.

## Additional Notes
The project presentations files, which include the architecture diagram and data-flow diagram can be found in the GitLab Wiki.

# Contributors
- Anjo Weddewer (aw181, 41486)
- Antti Kuivaleinen (ak366, 5010497)
- Elisa Zhang (ez018, 40972)
- Firaz Ilhan (fi007, 40032)
- Isaac Morales (im050, 44904)
- Johannes Rödel (jr125, 41959)