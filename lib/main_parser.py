#!/usr/bin/env python3

import re
import time
from requests.exceptions import SSLError
import base64
import warnings
from . import config
from .ansi_colors import *
from .results import results
from .alerts import error, alert_success, alert_time
import xml.etree.ElementTree as ET
from urllib.parse import urlparse, unquote

warnings.filterwarnings("ignore")

def make_request(headers, options, host, path):
    response = None
    try:
       
        # Extract protocol from a predefined configuration
        protocol = config.protocol

        # Construct the URL from the extracted components
        url = f'{protocol}://{host}{path}'

        try:
            response = options.session.get(url, headers=headers, proxies=options.proxies,
                                                allow_redirects=options.allow_redirects,
                                                verify=options.verify_tls, timeout=options.request_timeout)
            options.protocol = 'https'

        # Fall back to HTTP
        except SSLError:
            url_http = url.replace('https://', 'http://')

            response = options.session.get(url_http, headers=headers, proxies=options.proxies,
                                            allow_redirects=options.allow_redirects, verify=False, timeout=options.request_timeout)

            options.protocol = 'http'

    except Exception as e:

        error(e)

    if options.response:
        print(response.text)

    if (str(response.status_code)).startswith("30"):
        response_headers = response.headers
        
        for key, value in response_headers.items():
            if key == "Location":
                if value.startswith("https://wrongway.com") or value.startswith("http://wrongway.com"):
                    message = f"{url} - Status Code [{response.status_code}]"
                    alert_success(f"{url} - Status Code [{green}{response.status_code}{reset}]")
                    results(url, options.output_dir, message)
                    if not options.brute_force:
                        exit(1)
                else:
                    alert_time(f"{url} - Status Code [{red}{response.status_code}{reset}] (False-Positive)")
    else:
        alert_time(f"{url} - Status Code [{red}{response.status_code}{reset}]")

    rate_limit_seconds = options.rateLimit / 1000
    time.sleep(rate_limit_seconds)

def remove_keys_starting_with_prefix(dictionary, prefix):
    keys_to_remove = [key for key in dictionary.keys() if key.startswith(prefix)]
    for key in keys_to_remove:
        del dictionary[key]
    return dictionary


def extract_domain(url):
    parsed_url = urlparse(url)
    # Remove 'www.' if present and return the domain
    domain = parsed_url.netloc.replace('www.', '')
    return domain
    
def extract_domain_regex(string):
    domain_regex = r'(?:https?://)?(?:www\.)?([a-zA-Z0-9-]+\.[a-zA-Z]{2,})(?:\.[a-zA-Z]{2,})?'
    match = re.search(domain_regex, string)
    return match[1] if match else None

# Parsing headers from the request
def parse_headers(request):
    try:
        # Split the request into headers and body
        headers_end_index = request.find('\n\n')

        # If no double newline is found, try finding '\n\r\n'
        if headers_end_index == -1:
            headers_end_index = request.find('\n\r\n')

        # Extract the header content
        headers_content = request[:headers_end_index]

        # Extract headers using regular expression
        headers_list = re.findall(r'^(?P<name>[^:\r\n]+):\s*(?P<value>[^\r\n]*)', headers_content, flags=re.MULTILINE)

        # Convert the list of tuples to a list of dictionaries for easier manipulation
        headers_list = [{'key': key.strip(), 'value': value.strip()} for key, value in headers_list]

        # Convert the list of dictionaries to a dictionary
        headers = {item['key']: item['value'] for item in headers_list}

        headers = remove_keys_starting_with_prefix(headers, "GET")

        # Split the request string by lines
        lines = request.split('\n')

        # Extract the host value from the 'Host' header
        host = [line.split(': ')[1] for line in lines if line.startswith('Host')][0].split()[0]

        # Extract the path from the first line of the request
        path = lines[0].split(' ')[1]
        
        split_path = path.split("=")

        url_to_replace = ""

        # Detecting the redirected URL
        for value in split_path:
            
            # URL decoding the value
            decoded_value = unquote(value)

            if "http" in  decoded_value or "https" in decoded_value:

                url_to_replace = decoded_value
                domain_to_replace = extract_domain(url_to_replace)   
                break
        
        if url_to_replace == "":
            split_path.pop(0)
            for value in split_path:
                # URL decoding the value
                decoded_value = unquote(value)
                domain_to_replace = extract_domain_regex(decoded_value)

                if domain_to_replace is not None:
                    break
        
        keys_to_delete = []

        for key, value in headers.items():
            # Deleting unnecessary headers except cookies and authorization header
            if "Accept" in key:
                keys_to_delete.append(key)

        # Delete unnecessary headers
        for key in keys_to_delete:
            del headers[key]

        return headers, path, host, domain_to_replace

    except IndexError:
        error("A malformed request file was supplied, please check your request file.")

    except Exception as e:

        error(e)


def parse_request_file(request_file, options):
    try:
        try:
            request = ""  # Initialize an empty string to store the decoded request

            # Declaring an XML object and parsing the XML file
            tree = ET.parse(request_file)
            root = tree.getroot()

            for i in root:
                # Search for the 'request' element in the XML and extracting its text content
                request = i.find('request').text

                # Decode the base64 encoded content
                content = base64.b64decode(request)

                # Decode the content from latin-1 encoding
                request = content.decode('latin-1')

        except:
            # Open the request file as text
            with open(request_file, "r") as f:
                request = f.read()

        headers, path, host, domain_to_replace = parse_headers(request)

        return headers, path, host, domain_to_replace

    except Exception as e:

        error(e)