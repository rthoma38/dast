import os
import time
from zapv2 import ZAPv2

api_key = os.getenv('ZAP_API_KEY')  # Get the API key from the environment variable

# Use 'host.docker.internal' to allow communication between Docker and the host
zap_url = 'http://host.docker.internal:8081'
zap = ZAPv2(apikey=api_key, proxies={'http': zap_url, 'https': zap_url})

print("Ensuring ZAP is ready...")
time.sleep(10)

print("Starting a new session...")
zap.core.new_session(name='new_session', overwrite=True)

target = 'http://host.docker.internal:5000'  # Adjusted to allow Docker to access the target
print(f'Starting scan on target {target}')
zap.urlopen(target)  # Access the target URL

scan_id = zap.ascan.scan(target)
if not scan_id or scan_id == 'does_not_exist':
    print("Failed to start scan or invalid scan_id.")
    exit(1)

print(f"Scan ID: {scan_id}")

while True:
    scan_status = zap.ascan.status(scan_id)
    if scan_status == 'does_not_exist':
        print("Scan ID does not exist.")
        exit(1)
    
    try:
        scan_progress = int(scan_status)
    except ValueError as e:
        print(f"Error converting scan status to int: {e}")
        exit(1)
    
    print(f'Scan progress: {scan_progress}%')
    if scan_progress >= 100:
        break
    time.sleep(5)

print('Scan completed')

report = zap.core.htmlreport()
print(f'Report length: {len(report)}')
