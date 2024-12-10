import requests

#url for the authenticator api
auth_api_url = "https://web.socem.plymouth.ac.uk/COMP2001/auth/api/users"

#users emails and password to log in
auth_credentials = {
    "email": "ada@plymouth.ac.uk",
    "password": "insecurePassword"
}

#sending the log in details to the api
response = requests.post(auth_api_url, json=auth_credentials)

#checking to see weather log in was successful
if response.status_code == 200:
    print("User authenticated success")
    #looking at the information the api sent back
    response_data = response.json()
    print("Response JSON:", response_data) 

    #checking if the repsonce confirms the user is verified
    if isinstance(response_data, list) and 'Verified' in response_data and 'True' in response_data:
        print("User verification successful")
    else:
        print("User verification failed: Unexpected response format")
else:#printing the error if the login faled
    print("Authentication failed:", response.text)
