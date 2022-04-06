# gve_devnet_umbrella_top_destination_comparison
This sample code compares a customer's Top Destinations seen by Umbrella over a week time period to Umbrella's Top 1M, found here: http://s3-us-west-1.amazonaws.com/umbrella-static/index.html. The result is a CSV file saved to the C:/ drive that lists each customer destination that did not appear in Umbrella's Top 1M. 

## Contacts
* Erika Dietrick

## Solution Components
* Umbrella
* Windows

## Related Sandbox Environment
This sample code can be tested using a Cisco dCloud demo instance that contains Cisco Umbrella and a Windows VM. 

## Installation/Configuration
This project requires the following setup on the Windows machine: 
1. Install Python3
2. Install the *pandas* Python library with **pip install pandas**
3. Generate an Umbrella Reporting client ID and client secret by navigating to Umbrella > Admin > API Keys. *Please remember to copy your client secret; if you forget your client secret, you will need to generate a new client ID and secret.* 
4. Create a .env file as shown below:

```python
# Add the ID for your Umbrella organization, which can be found in the browser URL when accessing the Umbrella dashboard.
ORGANIZATION_ID=XXXXXXX
# Add the Umbrella Reporting client ID that you generated.
CLIENT_ID=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# Add the Umbrella Reporting client secret that you generated.
CLIENT_SECRET=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

```


## Usage
To run this script manually on a Windows computer, find the Command Prompt, right click, then choose Run as Administrator. *The script will only run as Administrator.*

In the command prompt, navigate to the directory where the script is saved, then enter the command **python TopDestinations.py**. 

The command prompt will print the following message when the script has completed successfully: 
"Domains that fell out of Umbrella's Top 1M this week can be found at C:/differences.csv."

To automate this script, you can create a task in Windows Task Scheduler: Start > Task Scheduler > right click Task Scheduler library > select New Folder > after naming folder, select the folder and then click the Action menu > Create Basic Task > choose Trigger based on customer needs > for Action, choose to Start a Program > specify the path of the script. *Using Task Scheduler requires at least Windows 10.*

# Screenshots

**Files saved to C: after script runs.**

![/IMAGES/FilesInCDrive.PNG](/IMAGES/FilesInCDrive.PNG)



**Sample contents of differences.csv, which shows Top Destinations that were not included in Umbrella's Top 1M, prompting investigation.**

![/IMAGES/SampleResultingCSV.PNG](/IMAGES/SampleResultingCSV.PNG)

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
