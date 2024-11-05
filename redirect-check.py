#Primarily created with OpenAI's ChatGPT 4o
#Checks a list of urls from a .csv for redirects

import requests
import csv
import time

# Paths to input and output files
input_file = "urls.csv"
output_file = "redirects.csv"

# Open the input file and output file
with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)
    
    # Write header for the output file
    writer.writerow(["Original URL", "Redirected URL", "Status Code", "Final URL"])
    
    # Loop through each URL
    for row in reader:
        url = row[0]
        try:
            # Print the URL being checked
            print(f"Checking URL: {url}")
            
            # Make a request to the URL and allow redirects
            response = requests.get(url, allow_redirects=True)
            status_code = response.status_code
            final_url = response.url
            redirected_url = final_url if final_url != url else ""

            # Write the result to the output file
            writer.writerow([url, redirected_url, status_code, final_url])

            # Print the status code and final URL
            print(f"Status: {status_code} | Final URL: {final_url}")

        except requests.RequestException as e:
            # If there's an error, log it
            writer.writerow([url, "Error", "", "Error: " + str(e)])
            print(f"Error with URL: {url} | {str(e)}")

        # Pause for a short time to avoid hitting the server too quickly
        time.sleep(1)  # Adjust the delay as needed

print("Redirect check complete! Results saved to", output_file)
