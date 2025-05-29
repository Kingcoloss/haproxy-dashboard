import re

def parse_log_file(log_file_path):
    parsed_entries = []
    xss_patterns = [
        r'<\s*script\s*',
        r'javascript:',
        r'<\s*img\s*src\s*=?',
        r'<\s*a\s*href\s*=?',
        r'<\s*iframe\s*src\s*=?',
        r'on\w+\s*=?',
        r'<\s*input\s*[^>]*\s*value\s*=?',
        r'<\s*form\s*action\s*=?',
        r'<\s*svg\s*on\w+\s*=?',
        r'script',
        r'alert',
        r'onerror',
        r'onload',
        r'javascript'
    ]

    sql_patterns = [
        r';',
        r'substring',
        r'extract',
        r'union\s+all',
        r'order\s+by',
        r'--\+',
        r'union',
        r'select',
        r'insert',
        r'update',
        r'delete',
        r'drop',
        r'@@',
        r'1=1',
        r'`1',
        r'union',
        r'select',
        r'insert',
        r'update',
        r'delete',
        r'drop',
        r'@@',
        r'1=1',
        r'`1'
    ]

    webshells_patterns = [
        r'payload',
        r'eval|system|passthru|shell_exec|exec|popen|proc_open|pcntl_exec|cmd|shell|backdoor|webshell|phpspy|c99|kacak|b374k|log4j|log4shell|wsos|madspot|malicious|evil.*\.php.*'
    ]

    combined_xss_pattern = re.compile('|'.join(xss_patterns), re.IGNORECASE)
    combined_sql_pattern = re.compile('|'.join(sql_patterns), re.IGNORECASE)
    combined_webshells_pattern = re.compile('|'.join(webshells_patterns), re.IGNORECASE)

    with open(log_file_path, 'r') as log_file:
        log_lines = log_file.readlines()
        for line in log_lines:
            if " 403 " in line:  # Check if the line contains " 403 " indicating a 403 status code
                match = re.search(r'(\w+\s+\d+\s\d+:\d+:\d+).*\s(\d+\.\d+\.\d+\.\d+).*"\s*(GET|POST|PUT|DELETE)\s+([^"]+)"', line)
                if match:
                    timestamp = match.group(1)  # Extract the date and time
                    ip_address = match.group(2)
                    http_method = match.group(3)
                    requested_url = match.group(4)

                    if combined_xss_pattern.search(line):
                        xss_alert = 'Possible XSS Attack Was Identified.'
                    else:
                        xss_alert = ''
                    if combined_sql_pattern.search(line):
                        sql_alert = 'Possible SQL Injection Attempt Was Made.'
                    else:
                        sql_alert = ''
                    if "PUT" in line:
                        put_method = 'Possible Remote File Upload Attempt Was Made.'
                    else:
                        put_method = ''

                    if "admin" in line:
                        illegal_resource = 'Possible Illegal Resource Access Attempt Was Made.'
                    else:
                        illegal_resource = ''

                    if combined_webshells_pattern.search(line):
                        webshell_alert = 'Possible WebShell Attack Attempt Was Made.'
                    else:
                        webshell_alert = ''

                    parsed_entries.append({
                        'timestamp': timestamp,
                        'ip_address': ip_address,
                        'http_method': http_method,
                        'requested_url': requested_url,
                        'xss_alert': xss_alert,
                        'sql_alert': sql_alert,
                        'put_method': put_method,
                        'illegal_resource': illegal_resource,
                        'webshell_alert': webshell_alert
                    })
    return parsed_entries