"""
CISCO SAMPLE CODE LICENSE Version 1.1 Copyright (c) 2020 Cisco and/or its affiliates

These terms govern this Cisco Systems, Inc. ("Cisco"), example or demo source code and its associated documentation 
(together, the "Sample Code"). By downloading, copying, modifying, compiling, or redistributing the Sample Code, you 
accept and agree to be bound by the following terms and conditions (the "License"). If you are accepting the License on 
behalf of an entity, you represent that you have the authority to do so (either you or the entity, "you"). Sample Code is 
not supported by Cisco TAC and is not tested for quality or performance. This is your only license to the Sample Code and all 
rights not expressly granted are reserved.

    LICENSE GRANT: Subject to the terms and conditions of this License, Cisco hereby grants to you a perpetual, 
    worldwide, non-exclusive, non- transferable, non-sublicensable, royalty-free license to copy and modify the 
    Sample Code in source code form, and compile and redistribute the Sample Code in binary/object code or other 
    executable forms, in whole or in part, solely for use with Cisco products and services. For interpreted languages 
    like Java and Python, the executable form of the software may include source code and compilation is not required.

    CONDITIONS: You shall not use the Sample Code independent of, or to replicate or compete with, a Cisco product or service. 
    Cisco products and services are licensed under their own separate terms and you shall not use the Sample Code in any way that 
    violates or is inconsistent with those terms (for more information, please visit: www.cisco.com/go/terms).

    OWNERSHIP: Cisco retains sole and exclusive ownership of the Sample Code, including all intellectual property rights 
    therein, except with respect to any third-party material that may be used in or by the Sample Code. Any such third-party 
    material is licensed under its own separate terms (such as an open source license) and all use must be in full accordance 
    with the applicable license. This License does not grant you permission to use any trade names, trademarks, service marks, 
    or product names of Cisco. If you provide any feedback to Cisco regarding the Sample Code, you agree that Cisco, its partners, 
    and its customers shall be free to use and incorporate such feedback into the Sample Code, and Cisco products and services, 
    for any purpose, and without restriction, payment, or additional consideration of any kind. If you initiate or participate in any 
    litigation against Cisco, its partners, or its customers (including cross-claims and counter-claims) alleging that the Sample Code 
    and/or its use infringe any patent, copyright, or other intellectual property right, then all rights granted to you under this License 
    shall terminate immediately without notice.

    LIMITATION OF LIABILITY: CISCO SHALL HAVE NO LIABILITY IN CONNECTION WITH OR RELATING TO THIS LICENSE OR USE OF THE SAMPLE CODE, 
    FOR DAMAGES OF ANY KIND, INCLUDING BUT NOT LIMITED TO DIRECT, INCIDENTAL, AND CONSEQUENTIAL DAMAGES, OR FOR ANY LOSS OF USE, DATA, 
    INFORMATION, PROFITS, BUSINESS, OR GOODWILL, HOWEVER CAUSED, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.

    DISCLAIMER OF WARRANTY: SAMPLE CODE IS INTENDED FOR EXAMPLE PURPOSES ONLY AND IS PROVIDED BY CISCO "AS IS" WITH ALL FAULTS AND WITHOUT 
    WARRANTY OR SUPPORT OF ANY KIND. TO THE MAXIMUM EXTENT PERMITTED BY LAW, ALL EXPRESS AND IMPLIED CONDITIONS, REPRESENTATIONS, 
    AND WARRANTIES INCLUDING, WITHOUT LIMITATION, ANY IMPLIED WARRANTY OR CONDITION OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE,
    NON- INFRINGEMENT, SATISFACTORY QUALITY, NON-INTERFERENCE, AND ACCURACY, ARE HEREBY EXCLUDED AND EXPRESSLY DISCLAIMED BY CISCO. 
    CISCO DOES NOT WARRANT THAT THE SAMPLE CODE IS SUITABLE FOR PRODUCTION OR COMMERCIAL USE, WILL OPERATE PROPERLY, IS ACCURATE OR COMPLETE,
    OR IS WITHOUT ERROR OR DEFECT.

    GENERAL: This License shall be governed by and interpreted in accordance with the laws of the State of California, excluding its conflict 
    of laws provisions. You agree to comply with all applicable United States export laws, rules, and regulations. If any provision of this 
    License is judged illegal, invalid, or otherwise unenforceable, that provision shall be severed and the rest of the License shall remain 
    in full force and effect. No failure by Cisco to enforce any of its rights related to the Sample Code or to a breach of this License in a 
    particular situation will act as a waiver of such rights. In the event of any inconsistencies with any other terms, this License shall 
    take precedence.
"""

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
