import time
import requests
import sys
import re
from urllib.parse import urlparse

# Define common admin paths to check
admin_paths = [
    "/admin", "/login", "/wp-admin", "/administrator", "/controlpanel",
    "/manage", "/backend", "/cms", "/dashboard", "/adminlogin", "/admin_area",
    "/siteadmin", "/useradmin", "/admincp", "/adminpanel", "/admincenter",
    "/adminconsole", "/admin_area", "/wp-login.php", "/admin.php", "/login.php",
    "/user.php", "/admin_login.php"
]

# Gradient colors
def gradient_text(text, colors):
    gradient_colors = colors
    result = ""
    for i, char in enumerate(text):
        color = gradient_colors[i % len(gradient_colors)]
        result += f"\033[38;5;{color}m{char}\033[0m"
    return result

# Define title and prompt with gradient
title = r"""
    ____        __  __       _______           __
   / __ \____ _/ /_/ /_     / ____(_)___  ____/ /__  _____
  / /_/ / __ `/ __/ __ \   / /_  / / __ \/ __  / _ \/ ___/
 / ____/ /_/ / /_/ / / /  / __/ / / / / / /_/ /  __/ /    
/_/    \__,_/\__/_/ /_/  /_/   /_/_/ /_/\__,_/\___/_/   
"""

prompt = "\033[35mEnter URL (e.g., http://example.com):\033[0m "

# Function to print text with a gradient effect
def print_gradient_text(text, colors):
    print(gradient_text(text, colors))

# Function to print the title, website link, warning, and prompt with a gradient effect
def print_gradient_title_and_prompt(title, prompt):
    gradient_colors_title = ["196", "202", "208", "214", "220", "226", "190", "184", "178", "172", "166", "160"]
    
    print(gradient_text(title, gradient_colors_title))
    print("\n\033[36mVisit our website: https://www.fontbees.store\033[0m")
    print("\033[33mWarning: This tool is for educational purposes only.\033[0m\n")
    sys.stdout.write(prompt)  # Write the prompt without a newline
    sys.stdout.flush()        # Ensure prompt is shown before input

# Function to validate URL
def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

# Function to check if URLs are available
def check_admin_paths(base_url):
    available_urls = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    
    for path in admin_paths:
        url = base_url.rstrip('/') + path
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                print(f"\033[38;5;82mAvailable: {url} [Status Code: 200 OK]\033[0m")
                available_urls.append(url)
            elif response.status_code == 403:
                print(f"\033[38;5;82mAvailable: {url} [Status Code: 403 Forbidden]\033[0m")
                available_urls.append(url)
            else:
                print(f"\033[38;5;196mChecked: {url} [Status Code: {response.status_code}]\033[0m")
        except requests.exceptions.RequestException as e:
            print(f"\033[38;5;196mError checking {url}: {e}\033[0m")
        time.sleep(1)  # Add a small delay between requests
    return available_urls

# Function to save the report of available URLs
def save_report(available_urls, output_file="available_admin_urls.txt"):
    with open(output_file, 'w') as f:
        for url in available_urls:
            f.write(f"{url}\n")
    print(f"\n\033[33mResults saved to {output_file}\033[0m")  # Print in yellow

# Main function to run the tool
def main():
    print_gradient_title_and_prompt(title, prompt)
    
    while True:
        base_url = input()  # Input on the same line as the prompt
        if is_valid_url(base_url):
            available_urls = check_admin_paths(base_url)
            available_count = len(available_urls)
            
            if available_count > 0:
                print(f"\n\033[33mAvailable URLs ({available_count}):\033[0m")
                for url in available_urls:
                    print(f"- \033[32m{url}\033[0m")  # Print URLs in green
                save_report(available_urls)
            else:
                print("\033[31mNo available admin URLs found.\033[0m")  # Print in red
            break
        else:
            print("\033[31mEnter a valid URL\033[0m")  # Print in red

if __name__ == "__main__":
    main()
