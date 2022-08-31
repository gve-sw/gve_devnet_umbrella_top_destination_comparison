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

import os.path
from pathlib import Path
from utils import get_top_million, create_aws_credentials, create_aws_config, sync_s3_bucket, \
    walk_dir_and_compare_top_million, convert_set_to_csv_file, valid_date, dir_path, valid_file
import pandas as pd
import datetime
from argparse import ArgumentParser

if __name__ == "__main__":
    """
    VARIABLES
    
    :final_csv_filename: string
    :final_directory_path: string
    :locally_synced_directory_name: string
    :top_million_url: string
    :daterange_start (optional): string 
    :daterange_end (optional): string
    """

    parser = ArgumentParser()

    parser.add_argument("-sd", "--start_date", dest="start_date", type=valid_date,
                        help="The start date (YYYY-MM-DD) of the DNS Logs to compare.",
                        default=None)

    parser.add_argument("-ed", "--end_date", dest="end_date", type=valid_date,
                        help="The end date (YYYY-MM-DD) of the DNS Logs to compare.",
                        default=None)

    parser.add_argument("-d", "--path", dest="path", type=dir_path,
                        help="The output directory path.",
                        default=Path.home())

    parser.add_argument("-f", "--filename", dest="filename", type=valid_file,
                        help="The filename of the outputted file.",
                        default="flagged_umbrella_domains.csv")

    args = parser.parse_args()

    # Start of the date range of the logs to compare (yyyy-mm-dd)
    if args.start_date is not None:
        daterange_start = str(args.start_date)
    else:
        daterange_start = args.start_date

    # End of the date range of the logs to compare (yyyy-mm-dd)
    if args.end_date is not None:
        daterange_end = str(args.end_date)
    else:
        daterange_end = args.end_date

    if daterange_start is not None:
        if daterange_end is None:
            daterange_end = datetime.datetime.today().strftime('%Y-%m-%d')

    # The name of the file returned after the program finishes
    final_csv_filename = args.filename

    # Points to home directory (windows: C:/, OSX/Linux: ~/)
    final_directory_path = str(args.path)

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

    # Walk the locally synced directory and compare domains to Umbrella's top million, returns a set of flagged domains
    final_domain_set = walk_dir_and_compare_top_million(directory_path=locally_synced_directory_name,
                                                        top_million_df=top_million_df,
                                                        daterange_start=daterange_start,
                                                        daterange_end=daterange_end)

    # Creates a CSV file of the flagged domains at the given filepath: final_directory_path+final_csv_filename
    convert_set_to_csv_file(s=final_domain_set, filepath=os.path.join(final_directory_path, final_csv_filename))
