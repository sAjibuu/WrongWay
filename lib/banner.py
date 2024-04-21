#!/usr/bin/env python3

# \033[1m is for a bold text
# \033[0m for a reset
# \033[1m\033[4m is for a bold and underline text

def banner():
    tool_banner = f"""\033[1m\033[0m
Wrongway is a simple tool for bypassing Open Redirect restrictions, created by Sagiv Michael.

\033[1mThe program only works with request files generated by proxy tools, such as Burp Suite and ZAP OWASP.\033[0m 

Usage: Wrongway [OPTIONS]

\033[1m\033[4mOptions:\033[0m
  \033[1m-h, --help\033[0m     Print help (see more with '--help')
  \033[1m-u, --usage\033[0m   Print the how to save the request file instructions.

\033[1m\033[4mRequired Arguments:\033[0m 
  \033[1m-f, --file\033[0m <REQUEST_FILE>    Provide a request file to be proccessed

\033[1m\033[4mRequest Settings:\033[0m 
  \033[1m--allow_redirects\033[0m     Follow redirects
  \033[1m-r, --response\033[0m        Print the response to the screen
  \033[1m-t, --time_out\033[0m <NUM>  Set the request timeout (Default is 8)
  \033[1m-c, --continue\033[0m        Continue testing even after a success
  \033[1m-rl, --rate_limit\033[0m <NUMBER>  Set a rate-limit with a delay in milliseconds between each request

\033[1m\033[4mProxy Settings:\033[0m 
  \033[1m-p, --proxy\033[0m <PROXY>   Proxy to use for requests (ex: http(s)://host:port, socks5(h)://host:port)
  \033[1m-k, --insecure\033[0m        Do not verify SSL certificates
  \033[1m--burp_http\033[0m           Set --proxy to 127.0.0.1:8080 and set --insecure to true (For HTTP requests)
  \033[1m--burp_https\033[0m          Set --proxy to 127.0.0.1:8080 and set --insecure to false (For HTTPs requests)

\033[1m\033[4mOptional Settings:\033[0m 
  \033[1m-o, --output\033[0m  <OUTPUT_PATH>    Output file to write the results into - Default current directory (ex: ~/Desktop/results.txt)
  \033[1m-d, --domain\033[0m  <domain_name>    Specify the allowed/intended domain that should redirect the user (Default - the domain from the host header)."""
    print(f"{tool_banner}")


def program_usage():
  reuqest_file_usage = """\nThe program only works with request files generated by proxy tools, such as Burp Suite and ZAP OWASP.
Save the request file from the proxy tool you are using, for example, in Burp Suite, choose "Save Item" or "Copy to file".
**Be aware** - If choosing "Copy to file", make sure to inspect the saved file, sometimes the file gets corrupted.
"""
  return reuqest_file_usage