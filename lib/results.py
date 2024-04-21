#!/usr/bin/env python3

import os
from .alerts import *
from urllib.parse import urlparse
from time import strftime

def results(url, output_folder, message):
    domain = get_domain_name(url)
    
    if not output_folder:
        folder_path = os.path.join(os.getcwd(), domain)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path, exist_ok=True)

        # Save the results to results.txt
        file_path = os.path.join(folder_path, "results.txt")
        f = open(f"{file_path}", "a")
        success(f"Results saved in {file_path}")

    else:
        f = open(output_folder, "a")

    now = strftime("%d/%m/%Y - %H:%M:%S")

    f.write("-------------------------------------------------------------------------------------------\n")
    f.write(
        f"[{now}] {message}\n")
    f.close()


def get_domain_name(url):
    parsed_url = urlparse(url)
    domain_name = parsed_url.netloc
    return domain_name