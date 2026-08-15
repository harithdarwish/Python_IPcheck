# --- STEP 1: READ AND CHECK OUR FILE.TXT ---
file_name = 'test1_IPcheckIPDB.txt'

with open(file_name, 'r', encoding='utf-8') as f:
    my_ips = [line.strip() for line in f if line.strip()]

print(f"Total IPs found: {len(my_ips)}")
print("-" * 30)

# 1. Show the Top 3
print("TOP 3 IPs:")
for ip in my_ips[:3]:
    print(f"  > {ip}")

print("-" * 30)

# 2. Show the Bottom 3
print("BOTTOM 3 IPs:")
for ip in my_ips[-3:]:
    print(f"  > {ip}")
    
#-----------------------------------------------------------------------------------------------------------------------------#
# --- STEP 2: CHECK API CONNECTIVITY ---
import requests

API_KEY = #YOUR_API_KEY
FILE_NAME = 'test1_IPcheckIPDB.txt'

def test_api():
    url = 'https://api.abuseipdb.com/api/v2/check'
    params = {'ipAddress': '8.8.8.8'} 
    headers = {
        'Accept': 'application/json',
        'Key': API_KEY 
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        print("API Success! Connection established.")
        return True
    else:
        print(f"API Failed. Error Code: {response.status_code}")
        # This will show the EXACT reason (e.g., "The API key is invalid")
        try:
            print(f"Server Message: {response.json()}")
        except:
            print(f"Server Message: {response.text}")
        return False

api_works = test_api()

#-----------------------------------------------------------------------------------------------------------------------------#
# --- STEP 3: GET TO KNOW API DATA (VARIABLE)---

import requests

url = 'https://api.abuseipdb.com/api/v2/check'
params = {'ipAddress': '8.8.8.8'} # You can test with any IP
headers = {
    'Accept': 'application/json',
    'Key': #YOUR_API_KEY
}

response = requests.get(url, headers=headers, params=params)

# This line prints the raw JSON list so you can see all the variable names
import pprint
pprint.pprint(response.json())

#-----------------------------------------------------------------------------------------------------------------------------#
# --- STEP 4: FETCH AND STORE ---
import sys
import requests  # Must be imported

MASTERIPDB_DATA = []

# Ensure api_works is defined from your previous test
if api_works:
    # --- READ FILE ---
    # This block is indented under 'if'
    with open(FILE_NAME, 'r') as file:
        ip_list = [line.strip() for line in file.readlines()]
        test_list = ip_list[:1000]       
    
    # INDENTED: These lines now belong to the 'if api_works' block
    total_ips = len(test_list)
    print(f"--- Starting Live Check for {total_ips} IPs ---")
    
    for index, ip in enumerate(test_list):
        # 1. LIVE COUNTER
        current_count = index + 1
        sys.stdout.write(f"\r🔍 Checking: {current_count} of {total_ips} ... (Current: {ip})")
        sys.stdout.flush()

        # 2. API REQUEST
        url = 'https://api.abuseipdb.com/api/v2/check'
        params = {'ipAddress': ip, 'maxAgeInDays': '90'}
        headers = {'Accept': 'application/json', 'Key': API_KEY} 
        
        try:
            response = requests.get(url, headers=headers, params=params)
            # Standardize: check for 200 OK before grabbing data
            if response.status_code == 200:
                data = response.json()['data']
                MASTERIPDB_DATA.append(data)
        except Exception as e:
            continue

    # 3. AFTER THE LOOP (Still indented under if api_works)
    print("\n\n✅ Live Check Complete!")
    print("-" * 40)
    
    if MASTERIPDB_DATA:
        print("--- PREVIEW (TOP 2) ---")
        for item in MASTERIPDB_DATA[:2]:
            print(f"IP: {item.get('ipAddress')} | Score: {item.get('abuseConfidenceScore')}% | {item.get('countryCode')}")
        
        print("\n... middle rows hidden ...\n")
        
        print("--- PREVIEW (BOTTOM 3) ---")
        for item in MASTERIPDB_DATA[-2:]:
            print(f"IP: {item.get('ipAddress')} | Score: {item.get('abuseConfidenceScore')}% | {item.get('countryCode')}")
    print("-" * 40)
else:
    print("❌ Error: api_works is False. Check your API key or connection.")

#-----------------------------------------------------------------------------------------------------------------------------#
# --- STEP 5: PRINT OUT THE API DATA (VARIABLE) AND ADJUST ACCORDING TO COLUMN. DOWNLOAD FILE.XLSX ---

import pandas as pd

# 1. Check if we actually have data
if not MASTERIPDB_DATA:
    print("No data found in MASTERIPDB_DATA. Please run Step 3 first!")
else:
    # 2. Convert the list of dictionaries into a DataFrame (Table)
    df = pd.DataFrame(MASTERIPDB_DATA)

    # 3. Select and Rename the columns to make them look nice
    # We pick the most important ones based on your variables
    columns_to_keep = {
        'ipAddress': 'IP Address',
        'countryCode': 'Country',
        'isp': 'ISP',  # One ISP can own multiple ASN
        'totalReports': 'Total Reports',
        'abuseConfidenceScore': 'Abuse Score (%)',
    }
    
    # Filter the table to only show the columns we want
    df_final = df[list(columns_to_keep.keys())].rename(columns=columns_to_keep)

    # 4. Save to Excel
    output_file = "AbuseIPDB_Report.xlsx"
    df_final.to_excel(output_file, index=False)

    print(f"Success! Your Excel file is ready.")
    print(f"File Name: {output_file}")
    
    # 5. Preview the first few rows in your notebook
    display(df_final.head())
