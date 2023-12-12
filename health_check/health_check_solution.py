import requests
import yaml
import time
from collections import defaultdict
from signal import signal, SIGINT
from sys import exit

# Function to handle Ctrl+C
def handler(signal_received, frame):
    print("\nExiting program.")
    exit(0)

# Function to send HTTP request and check health
def check_health(endpoint):
    try:
        response = requests.request(
            method=endpoint.get('method', 'GET'),
            url=endpoint['url'],
            headers=endpoint.get('headers', {}),
            data=endpoint.get('body', ''),
            timeout=5
        )
        latency = response.elapsed.total_seconds() * 1000  # in milliseconds

        if 200 <= response.status_code < 300 and latency < 500:
            return 'UP', latency
        else:
            return 'DOWN', latency
    except Exception as e:
        return 'DOWN', 0

# Function to calculate availability percentage
def calculate_availability(health_results):
    availability = {}
    for domain, results in health_results.items():
        total = len(results)
        up_count = sum(1 for status, _ in results if status == 'UP')
        percentage = round((up_count / total) * 100) if total > 0 else 0
        availability[domain] = percentage
    return availability

# Function to log availability percentage
def log_availability(availability):
    for domain, percentage in availability.items():
        print(f"{domain} has {percentage}% availability percentage")

if __name__ == "__main__":
    signal(SIGINT, handler)
    
    # Read YAML configuration file
    file_path = input("Enter the path to the YAML configuration file: ")
    with open(file_path, 'r') as file:
        endpoints = yaml.safe_load(file)

    # Group endpoints by domain
    domain_endpoints = defaultdict(list)
    for endpoint in endpoints:
        domain = endpoint['url'].split('/')[2]
        domain_endpoints[domain].append(endpoint)

    # Perform health checks every 15 seconds
    health_results = defaultdict(list)
    while True:
        for domain, endpoints in domain_endpoints.items():
            for endpoint in endpoints:
                status, latency = check_health(endpoint)
                health_results[domain].append((status, latency))

        # Calculate and log availability percentage
        availability = calculate_availability(health_results)
        log_availability(availability)

        time.sleep(15)
