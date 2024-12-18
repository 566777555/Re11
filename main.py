import requests
import random
import time

def send_messages_with_auto_dismiss():
    # Read tokens, conversation ID, and messages from files
    with open('tokennum.txt', 'r') as file:
        tokens = file.readlines()

    with open('convo.txt', 'r') as file:
        convo_id = file.read().strip()

    with open('File.txt', 'r') as file:
        messages = file.readlines()

    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0.0; Samsung Galaxy S9 Build/OPR6.170623.017; wv) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.125 Mobile Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
        'referer': 'www.google.com'
    }

    # Auto-dismiss handling loop
    for token in tokens:
        access_token = token.strip()
        print(f"[INFO] Using Token: {access_token}")

        for message in messages:
            message = message.strip()
            url = f"https://graph.facebook.com/v17.0/t_{convo_id}"
            parameters = {'access_token': access_token, 'message': message}

            try:
                response = requests.post(url, json=parameters, headers=headers)
                response_data = response.json()

                if response.status_code == 200:
                    print(f"[+] Message sent successfully with token {access_token}: {message}")
                else:
                    # Check if automated behavior warning is present
                    if 'error' in response_data and 'automated behavior' in response_data['error']['message']:
                        print(f"[WARNING] Automated behavior detected for token {access_token}. Skipping this token.")
                        break  # Exit loop for this token
                    else:
                        print(f"[ERROR] Failed to send message with token {access_token}: {response_data['error']['message']}")

            except Exception as e:
                print(f"[EXCEPTION] An error occurred: {e}")

            # Random delay to mimic human behavior
            time.sleep(random.randint(5, 15))

        print(f"[INFO] Completed sending messages for token: {access_token}")
        print("-" * 50)

    print("[INFO] All tokens processed.")

# Call the function
send_messages_with_auto_dismiss()
