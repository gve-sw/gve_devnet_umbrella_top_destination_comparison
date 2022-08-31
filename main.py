import os.path
from pathlib import Path
from utils import get_top_million, create_aws_credentials, create_aws_config, sync_s3_bucket, \
    walk_dir_and_compare_top_million, convert_set_to_csv_file
import pandas as pd

if __name__ == "__main__":

    """
    VARIABLES
    
    :final_csv_filename: string
    :final_directory_path: string
    :locally_synced_directory_name: string
    """
    # The name of the file returned after the program finishes
    final_csv_filename = "flagged_umbrella_domains.csv"

    # Points to home directory (windows: C:/, OSX/Linux: ~/)
    final_directory_path = str(Path.home())

    # Locally synced directory name ('dnslogs' by default)
    locally_synced_directory_name = "dnslogs"

    top_million_url = "http://s3-us-west-1.amazonaws.com/umbrella-static/top-1m.csv.zip"


    """
    This program has the following workflow:
     1. Downloads Umbrella's top million domains from the "top_million_url"
     2. Creates AWS credentials using the user provided environment variables in .env file
     3. Downloads/syncs your Umbrella DNS logs from AWS to your local machine
     4. Compares your Umbrella DNS logs to Umbrella's Top million DNS domains
     5. Creates a CSV file of all the DNS domains NOT found in Umbrella's Top million DNS domains
    
    """

    # Grabs the top million domains from Umbrella (AWS Bucket) and saves it as a zipped .csv file
    top_million_filepath = get_top_million(top_million_url=top_million_url)

    # Convert Umbrella's top million domain CSV to Pandas dataframe
    top_million_df = pd.read_csv(top_million_filepath, header=None)

    # Create AWS credentials (by default it reads the environment variables given in .env file)
    create_aws_credentials()

    # Create AWS config (by default it reads the environment variables given in .env file)
    create_aws_config()

    # Syncs your umbrella account's AWS datapath to a local directory.
    sync_s3_bucket()

    # Walk the locally synced directory and compare domains to Umbrella's top million and return a set of flagged domains
    final_domain_set = walk_dir_and_compare_top_million(directory_path=locally_synced_directory_name,
                                                        top_million_df=top_million_df)


    # Creates a CSV file of the flagged domains at the given filepath: final_directory_path+final_csv_filename
    convert_set_to_csv_file(s=final_domain_set, filepath=os.path.join(final_directory_path, final_csv_filename))
