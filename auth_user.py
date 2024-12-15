#import requests

# URL for the authenticator API
#auth_api_url = "https://web.socem.plymouth.ac.uk/COMP2001/auth/api/users"

#def authenticate_user(email, password):
 #   auth_credentials = {
  #      "email": email,
   #     "password": password
    #}
    #
    #response = requests.post(auth_api_url, json=auth_credentials)
    
    # Checking if the login was successful
    #if response.status_code == 200:
     #   response_data = response.json()
      #  print("Debug: Auth Response Data:", response_data)  # Debugging statement
       # if isinstance(response_data, list) and 'Verified' in response_data and 'True' in response_data:
        #    return True  # User is authenticated and verified
        #else:
         #   return False  # User verification failed
    #else:
     #   return False  # Authentication failed


#def is_admin_user(email, password):
 #   auth_credentials = {
  #      "email": email,
   #     "password": password
    #}
    
    #response = requests.post(auth_api_url, json=auth_credentials)
    
    #if response.status_code == 200:
     #   try:
      #      response_data = response.json()
       #     print("Debug: Response Data Type:", type(response_data))  # Log the type of response data
        #    print("Debug: Raw Response Data:", response_data)  # Log the raw response data
            
         #   admin_users = ["ada@plymouth.ac.uk", "tim@plymouth.ac.uk"]
            
          #  if isinstance(response_data, list):
           #     print("Debug: Response is a list")
            #    for user in response_data:
             #       print("Debug: User Object:", user)
              #  return any(user.get('Email') in admin_users for user in response_data)
            
            #elif isinstance(response_data, dict):
             #   print("Debug: Response is a dict")
              #  return response_data.get('Email') in admin_users
            
            #else:
             #   print("Debug: Unexpected response format:", response_data)
              #  return False
        
        #except ValueError:
         #   print("Failed to parse JSON response")
          #  return False
    #else:
     #   print(f"Failed to authenticate. Status code: {response.status_code}, Response: {response.text}")
      #  return False
