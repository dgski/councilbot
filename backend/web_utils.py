from fastapi import Header
import requests

# Get a valid token from the cron service api
def get_valid_token(cronservice_url: str, job_token : str) -> bool:
    try:
        response = requests.get(f'{cronservice_url}/confirm?jobToken={job_token}')
        if response == None or response.status_code != 200:
            raise RuntimeError('invalidToken')
    except Exception as e:
        return None
    return True

# Dependency to determine allowed origins dynamically
def get_allowed_origins(origin: str = Header(None)):
    # Implement your logic here to calculate allowed origins based on the request
    if origin:
        # You can add custom logic to validate the origin
        return [origin]
    else:
        return []