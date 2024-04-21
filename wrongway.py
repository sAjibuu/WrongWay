#!/usr/bin/env python3

# Made by Sagiv

# Wrongway is a simple tool for bypassing Open Redirect restrictions.

# Copyright (C) 2024 Sagiv Michael

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# importing necessary modules
import argparse
import requests
from lib.banner import banner, program_usage
from lib import alerts
from lib.main_parser import parse_request_file
import sys
import time
import importlib
import lib.config as config

class Wrongway:
    def __init__(self, user_options) -> None:

        # Initialize variables
        self.options = user_options
        self.request_file = user_options.request_file
        self.proxy = user_options.proxy
        self.verify_tls = user_options.insecure
        self.burp_http = user_options.burp_http
        self.burp_https = user_options.burp_https
        self.session = requests.Session()


    # User arguments
    @staticmethod
    def args():

        parser = argparse.ArgumentParser(add_help=False)

        # Check if the user explicitly requests help
        if "-h" in sys.argv or "--help" in sys.argv or len(sys.argv) == 1:
            banner()
            sys.exit()

        # User Options
        parser.add_argument("-f", "--file", required=False, default="not_set", dest="request_file")
        parser.add_argument("-d", "--domain", type=str, dest="domain_name", required=False, default=False)
        parser.add_argument("-o", "--output", type=str, dest="output_dir", required=False, default=False)
        parser.add_argument("-rl", "--rate_limit", type=int, dest="rateLimit", required=False, default=0)
        parser.add_argument("-p", "--proxy", type=str, dest="proxy", required=False, default="optional")
        parser.add_argument("-k", "--insecure", action="store_false", dest="insecure", required=False)
        parser.add_argument("-r", "--response", action="store_true", required=False, dest="response")
        parser.add_argument("-t", "--time_out", type=int, default=8, required=False, dest="request_timeout")
        parser.add_argument("--base64", action="store_true", required=False, dest="base64")
        parser.add_argument("--burp_http", action="store_true", required=False, dest="burp_http")
        parser.add_argument("--burp_https", action="store_true", required=False, dest="burp_https")
        parser.add_argument("--allow_redirects", action="store_true", required=False, dest="allow_redirects")
        parser.add_argument("-c", "--continue", action="store_true", required=False, dest="brute_force")
        parser.add_argument("-u", "--usage", action="store_true", dest="usage")

        return parser.parse_args()


    def main(self):
        try:

            if self.request_file == 'not_set':
                alerts.error(f"-r, --request_file is a required argument!")

            if not self.verify_tls:
                # Disable SSL verification 
                options.verify_tls = False

            else:
                # Enable SSL verification 
                options.verify_tls = True

            # Check if proxy is provided and valid
            if self.proxy != 'optional':
                if self.proxy.startswith("http://"):
                    self.proxy = self.proxy.replace("http://", "")
                elif self.proxy.startswith("https://"):
                    self.proxy = self.proxy.replace("https://", "")

                alerts.info(f"Proxy is running on {self.proxy}")

                if self.proxy.startswith("socks"):
                    proxy_url = self.proxy.replace("socks://", "")
                    options.proxies = {
                        'http': f'socks5://{proxy_url}',
                        'https': f'socks5://{proxy_url}'
                    }
                else:
                    options.proxies = {
                        'http': self.proxy,
                        'https': self.proxy
                    }

            else:
                options.proxies = options.proxies = {
                    'http': None,
                    'https': None,
                }

            if self.burp_http or self.burp_https:
                alerts.info(f"Proxy is running on 127.0.0.1:8080")
                options.proxies = {
                    'http': "127.0.0.1:8080",
                    'https': "127.0.0.1:8080",
                }

                if self.burp_http:
                    options.verify_tls = True
                elif self.burp_https:
                    options.verify_tls = False

            # Check if arguments supplied by the user is less than 2
            if len(sys.argv) < 2:
                print("Try '-h or --help' for more information.")
                sys.exit(1)

            # Define session withing the argsparse namespace, for an ease use later
            options.session = self.session

            # Include or Exclude modules
            all_modules = config.active_modules
            modules_without_slash = config.modules_without_slash

            final_modules = importlib.import_module("lib.modules")

            headers, path, host, domain_to_replace = parse_request_file(self.request_file, options)

            if not options.domain_name:
                domain = host
            else:
                domain = options.domain_name

            if "http" in path:
                for module in all_modules:
                    # Execute each module with its necessary arguments
                    getattr(final_modules, module)(path, headers, host, domain, options, domain_to_replace)
            else:
                for module in modules_without_slash:
                    # Execute each module with its necessary arguments
                    getattr(final_modules, module)(path, headers, host, domain, options, domain_to_replace)

            if "http" in path:
                alerts.info("Trying without HTTP/s protocol...")
                time.sleep(1)
                path = path.replace("http://", "").replace("https://", "")
            
            else:
                alerts.info("Trying with HTTP/s protocol...")
                path = path.replace(domain_to_replace, f"{config.protocol}://{domain_to_replace}")
                        
            if "http" in path:
                for module in all_modules:
                    # Execute each module with its necessary arguments
                    getattr(final_modules, module)(path, headers, host, domain, options, domain_to_replace)
            else:
                for module in modules_without_slash:
                    # Execute each module with its necessary arguments
                    getattr(final_modules, module)(path, headers, host, domain, options, domain_to_replace)

        except KeyboardInterrupt:
            alerts.error("Caught CTRL + C. Exiting...")

        except Exception as error:

            alerts.error(error)

# Main function with all its arguments parsing
if __name__ == "__main__":

    try:
        options = Wrongway.args()

        usage = options.usage
        session = requests.Session()

        if usage:
            print(program_usage())
            sys.exit(0)

        # Create an instance of Wrongway
        Wrongway = Wrongway(options)
        # Call main function
        Wrongway.main()

    except Exception as e:
            
        alerts.error(e)

    except KeyboardInterrupt:
        alerts.error("Caught CTRL + C. Exiting...")