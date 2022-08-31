# gve_devnet_umbrella_top_destination_comparison
This sample code compares a customer's Top Destinations seen by Umbrella over a week time period to Umbrella's Top 1M, found here: http://s3-us-west-1.amazonaws.com/umbrella-static/index.html. The result is a CSV file saved to the homepath that lists each customer destination that did not appear in Umbrella's Top 1M. 

## Contacts
* Charles Llewellyn

## Solution Components
* Umbrella

## Related Sandbox Environment
This sample code can be tested using a Cisco dCloud demo instance that contains Cisco Umbrella. 

## Installation/Configuration
This project requires the following setup: 
1. Install Python3
2. Install pip3 (if not installed with python3)
3. Create virtual environment

   ``` python3 -m venv venv```
   
4. Activate vitrual environment:

   OSX/Linux:
      
      ```source venv/bin/activate```
      
   Windows:
      
      ```venv\Scripts\activate```
  
5. Upgrade pip3

    ```pip3 install --upgrade pip```
  
6. Install script requirements

    ```pip3 install -r requirements.txt```
 
7. Enable Umbrella logging to Cisco Managed AWS bucket: https://docs.umbrella.com/deployment-umbrella/docs/cisco-managed-s3-bucket
8. Modify the .env file variables with the correct information (Given after completing step 7):

```python
# Add Datapath to the AWS S3 Bucket for Umbrela logs
DATA_PATH=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# Add the Access Key for the AWS S3 Bucket
ACCESS_KEY=XXXXXXXXXXXXXXXXXXXX
# Add the Secret Key for the AWS S3 Bucket
SECRET_KEY=XXXXXXXXXXXXXXXXXXXX

```


## Usage
To run this script run the following command:

   ``` python main.py```

Optional arguments:

     -h, --help            show this help message and exit
     -sd START_DATE, --start_date START_DATE
                           The start date (YYYY-MM-DD) of the DNS Logs to compare.
     -ed END_DATE, --end_date END_DATE
                           The end date (YYYY-MM-DD) of the DNS Logs to compare.
     -d PATH, --path PATH  The output directory path.
     -f FILENAME, --filename FILENAME
                           The filename of the outputted file.
   



# Screenshots

![/IMAGES/0image.png](/IMAGES/0image.png)

### LICENSE

Provided under Cisco Sample Code License, for details see [LICENSE](LICENSE.md)

### CODE_OF_CONDUCT

Our code of conduct is available [here](CODE_OF_CONDUCT.md)

### CONTRIBUTING

See our contributing guidelines [here](CONTRIBUTING.md)

#### DISCLAIMER:
<b>Please note:</b> This script is meant for demo purposes only. All tools/ scripts in this repo are released for use "AS IS" without any warranties of any kind, including, but not limited to their installation, use, or performance. Any use of these scripts and tools is at your own risk. There is no guarantee that they have been through thorough testing in a comparable environment and we are not responsible for any damage or data loss incurred with their use.
You are responsible for reviewing and testing any scripts you run thoroughly before use in any non-testing environment.
