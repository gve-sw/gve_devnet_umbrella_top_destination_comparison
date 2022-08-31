import os
import os.path
from dotenv import load_dotenv
from pathlib import Path
import re
import subprocess
import pandas as pd
import requests

load_dotenv()
# Credentials found in .env file
region_regex = "cisco-managed-(.*)/"
datapath = os.environ.get("DATA_PATH")
access_key = os.getenv("ACCESS_KEY")
secret_key = os.getenv("SECRET_KEY")
region = None
if datapath:
    region = re.search(region_regex, datapath)
    if region:
        region = region.group(1)
        print(f"AWS Region: {region}")


# Download the Umbrella top 1 million destinations to home directory, unzip file,
# and format CSV to be compared with organizaton's Top Destinations CSV.
def get_top_million(top_million_url):
    """
    Takes the given top_million_url and downloads the file as a zip file.
    Returns the filepath to the newly created zipfile.

    Parameters
    ----------
    top_million_url: string

    Returns
    -------
    top_million_filepath: string

    """
    file_path = str(Path.home())
    get_file = requests.get(top_million_url)
    top_million_filepath = os.path.join(".", 'top-1m.csv.zip')

    with open(top_million_filepath, 'wb') as f:
        f.write(get_file.content)

    return top_million_filepath


def create_aws_credentials(access_key=access_key, secret_key=secret_key):
    """
    Creates the AWS credentials file for the AWS CLI.

    Parameters
    ----------
    access_key: AWS Access Key: string
    secret_key: AWS Secret Key: string

    Returns
    -------
    Null
    """

    home_path = str(Path.home())
    os.makedirs(os.path.join(home_path, ".aws"), exist_ok=True)
    with open(os.path.join(home_path, ".aws", "credentials"), 'w') as f:
        f.write("[default]\n")
        f.write(f"aws_access_key_id = {access_key}\n")
        f.write(f"aws_secret_access_key = {secret_key}")


def create_aws_config(region=region):
    """
    Creates the AWS configuration file for the AWS CLI

    Parameters
    ----------
    region: AWS Region of Umbrella DNS logs bucket: string

    Returns
    -------
    Null

    """
    home_path = str(Path.home())
    os.makedirs(os.path.join(home_path, ".aws"), exist_ok=True)
    with open(os.path.join(home_path, ".aws", "config"), 'w') as f:
        f.write("[default]\n")
        f.write(f"region={region}")


def sync_s3_bucket(datapath=datapath):
    """
    Downloads/syncs the Umbrella DNS logs found at the given datapath

    Parameters
    ----------
    datapath: AWS datapath to Umbrella DNS logs bucket: string

    Returns
    -------
    Null
    """
    sync_command = f"aws s3 sync s3://source-bucket/ s3://destination-bucket/"
    subprocess.run(['aws', 's3', 'sync', f"s3://{datapath}", '.'])


def walkdir(dirname):
    """
    Walks through each directory in the given directory filepath (dirname) and
    yields a Pandas dataframe of the csv files found in each directory

    Parameters
    ----------
    dirname: Path to the directory containing Umbrella dnslogs: string

    Returns
    -------

    """
    for cur, _dirs, files in os.walk(dirname):
        pref = ''
        head, tail = os.path.split(cur)
        while head:
            pref += '---'
            head, _tail = os.path.split(head)
        print(pref + tail)
        for f in files:
            if ".DS_Store" not in f:
                print(tail + '---' + f)
                dnslog = pd.read_csv(f"{dirname}/{tail}/{f}", header=None)
                yield dnslog


def compare_columns(local_df, top_df):
    """
    Compares the local_df's domains to Umbrella's top million domains and
    returns local domains that have not been found in Umbrella's top million domain dataframe.

    Parameters
    ----------
    local_df: The pandas dataframe of the local DNS logs csv file: string
    top_df: The pandas dataframe of Umbrella's top million csv file: string

    Returns
    -------
    non_matched_domains: set

    """
    non_matched_domains = set()
    for domain in local_df.iloc[:, 8]:
        if "." == domain[-1]:
            domain = domain[:-1]
        if domain not in top_df.values:
            non_matched_domains.add(domain)

    return non_matched_domains


def walk_dir_and_compare_top_million(directory_path, top_million_df):
    """
    Walks the directory found at "directory_path" and compares all DNS log CSV files
    found within subsequent directories. Returns a set of all domains that did not match
    with Umbrella's top million DNS domains.

    Parameters
    ----------
    directory_path
    top_million_df

    Returns
    -------
    domain_set: set


    """
    domain_set = set()
    for csv in walkdir(directory_path):
        domains = compare_columns(csv, top_million_df)
        domain_set.update(domains)

    return domain_set


def convert_set_to_csv_file(s, filepath):
    """
    Converts a given set, s, into a .csv file at the given filepath

    Parameters
    ----------
    s: set
    filepath: string

    Returns
    -------
    Null

    """
    s = list(s)
    df = pd.DataFrame(s)
    df.to_csv(filepath)
