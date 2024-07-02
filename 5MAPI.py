import json
import os
import requests
import random
from fake_useragent import UserAgent
from colorama import init, Fore, Style


init(autoreset=True)

url = {"api": ""}
fname = {"name": ""}

def menu():
    print("""

    Example link is : https://servers-frontend.fivem.net/api/servers/single/5lamjz

    NB! This tool is not project it is for data testing for FiveM
    
    """)
    inp1 = input("Enter FiveM Server API: ")
    inp2 = input("Enter filename to specify:")
    url["api"] = inp1
    fname["name"] = inp2

# Data from API
def fetch_data_from_api(api_url):
    try:
        ua = UserAgent()
        headers = {'User-Agent': ua.random}
        
        # GET request sender
        response = requests.get(api_url, headers=headers)
        
        # request control
        if response.status_code == 200:
            # Parse JSON response
            data = response.json()
            return data
        elif response.status_code == 403:
            print(Fore.RED + "Error: Access Forbidden. Check API permissions or authentication.")
            return None
        else:
            print(Fore.RED + f"Error: Unable to fetch data. Status code {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Error: {e}")
        return None

# To JSON file
def save_data_to_json(data, folder, filename):
    try:
        os.makedirs(folder, exist_ok=True)  # Create folder if it doesn't exist
        filepath = os.path.join(folder, filename)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)
        print(Fore.YELLOW + f"Data saved to {filepath} successfully.")
    except Exception as e:
        print(Fore.RED + f"Error saving data to {filepath}: {e}")




if __name__ == "__main__":
    menu()  # menu init
    api_url = url["api"]  # Get url
    
    if api_url:
        api_data = fetch_data_from_api(api_url)
        
        if api_data:
           
            #print(Fore.YELLOW + "Fetched Data:")
            #print(json.dumps(api_data, indent=4))
            
           
            folder_name = 'fivem_data'  

            filename = f'{fname["name"]}.json' 
            save_data_to_json(api_data, folder_name, filename)
            
            # Extract data
            endpoint = api_data.get("Data", {}).get("connectEndPoints", [])[0]  # Adjust to your actual JSON structure
            server_name = api_data.get("Data", {}).get("hostname")
            players = api_data.get("Data", {}).get("players")
            
            if endpoint:
                print(Fore.GREEN + f"IP: {endpoint}")
            if server_name:
                print(Fore.YELLOW + f"Server Name: {server_name}")
            if players:
                print(Fore.YELLOW + f"Number of Players: {len(players)}")
           
        else:
            print(Fore.RED + "Failed to fetch data from API.")
    else:
        print(Fore.RED + "Invalid URL provided.")
