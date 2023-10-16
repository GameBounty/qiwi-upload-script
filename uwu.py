import subprocess
import json
import urllib.parse
import argparse
import threading
import re

parser = argparse.ArgumentParser(description='Upload a file to the qiwi API')
parser.add_argument('file_path', help='python uwu.py "your file path"')

args = parser.parse_args()

#opens your funny wunny account info from le json file
with open('uwu.json', 'r') as json_file:
    uwu = json.load(json_file)
    
#change your valueable account into HTML percent-encoded notation for the API request
uwu1 = urllib.parse.quote(uwu["email"])
uwu2 = urllib.parse.quote(uwu["password"])

#the curl command which wont need much changing ever
funnycurlmoment = f'curl -X POST https://api.qiwi.gg/auth -H "Content-Type: application/x-www-form-urlencoded" -d "email={uwu1}&password={uwu2}"'

def track_progress(process):
    upload_progress = re.compile(r'(\d+)\s+%')
    progress = 0

    for line in process.stdout:
        match = upload_progress.search(line)
        if match:
            new_progress = int(match.group(1))
            if new_progress > progress:
                print(f"Progress: {new_progress}%")
                progress = new_progress

def capture_output(process):
    for line in process.stdout:
        pass

def capture_error(process):
    for line in process.stderr:
        print(line, end="")


#run the command (with rizz) and checks for errors
try:
    result = subprocess.run(funnycurlmoment,shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    if result.returncode == 0:
        print("we did it we got the auth token")
        resp = json.loads(result.stdout)
        token = resp.get('token')
        if token:
            funnycurlmomentparttwo = f'curl -X POST -H "Authorization: Bearer {token}" -F "file=@{args.file_path}" https://api.qiwi.gg/upload/file'

            upload_process = subprocess.Popen(funnycurlmomentparttwo,shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
            

            progress_thread = threading.Thread(target=track_progress, args=(upload_process,))
            output_thread = threading.Thread(target=capture_output, args=(upload_process,))
            error_thread = threading.Thread(target=capture_error, args=(upload_process,))

            progress_thread.start()
            output_thread.start()
            error_thread.start()

            progress_thread.join()
            output_thread.join()
            error_thread.join()
            if upload_process.returncode == 0:
                print("upload complete probably")
            else:
                print("it probably worked but im too dumb to finish this tonight, will be updated when i feel like it for now just check your qiwi account")
                print(upload_process.stderr)
        else:
            print("Token not found grrr")
    else:
        print("send this error to zero")
        print(result.stderr)
        
except Exception as e:
    print(f"oopsies woopsies we ran into an error: {str(e)}")