import requests
import pandas as pd

def send_contacts(file_path):
    url = "http://localhost:8002/contacts/api/create_contacts/"
    headers = {
        "Authorization": "Token 7545693aab566e5a4b37cdbbaa0de3cc13cff4e1"
    }
    
    # Define default values
    default_gender = "مرد"
    default_group_id = "4"
    
    # Read contacts from the Excel file
    try:
        contacts_df = pd.read_excel(file_path)
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return
    
    for _, row in contacts_df.iterrows():
        # Extract data for each contact
        data = {
            "first_name": row.get("First_Name", ""),
            "last_name": row.get("Last_Name", ""),
            "phone_number": f"0{row.get("phone_number", "")}",
            "gender": default_gender,
            "group_id": default_group_id
        }
        print(data)
        try:
            response = requests.post(url, headers=headers, data=data)
            if response.status_code == 200:
                print(f"Contact {data['first_name']} {data['last_name']} created successfully!")
            else:
                print(f"Failed to create contact {data['first_name']} {data['last_name']}. Status code: {response.status_code}")
                print("Response:", response.status_code)
        except Exception as e:
            print(f"An error occurred: {e}")
file_path = "Contact-2024-11-20.xlsx"

# Run the function with the file path
send_contacts(file_path)
