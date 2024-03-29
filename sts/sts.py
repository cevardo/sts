import sys
import json
import os
from dotenv import load_dotenv
load_dotenv()

credentials_file_path = os.getenv("credentials_file_path")
arn = os.getenv("arn")
master_aws_access_key_id = os.getenv("master_aws_access_key_id")
master_aws_secret_access_key = os.getenv("master_aws_secret_access_key")

# START
os.system("echo *** Running STS Configuration Script ***")

tokenCode = str(sys.argv[1])
os.system("echo Token Code: " + tokenCode)

try:
    # Execute AWS CLI command to retrieve STS token
    command = os.system('aws sts get-session-token --serial-number ' +
                        arn + ' --profile master --token-code ' + tokenCode + ' 1>out.txt')

    # Store generated keys
    tempJsonFile = 'out.txt'
    with open(tempJsonFile) as json_file:
        data = json.load(json_file)
    print(data)

    # Create or replace credentials file
    with open(credentials_file_path, 'w') as credentialsFile:
        content = [
            "[default]",
            "aws_access_key_id = " + data['Credentials']['AccessKeyId'],
            "aws_secret_access_key = " +
            data['Credentials']['SecretAccessKey'],
            "aws_session_token = " + data['Credentials']['SessionToken'],
            "[master]",
            "aws_access_key_id = " + master_aws_access_key_id,
            "aws_secret_access_key = " + master_aws_secret_access_key
        ]
        credentialsFile.writelines("%s\n" % line for line in content)
        credentialsFile.close()

    print("Credentials file updated!")
except Exception as err:
    print("STS Token generation failed!\nMeet the following prerequisites to proceed:\n  - Connect to cloudvpn.cms.gov\n  - Have BIC AWS permissions granted\n  - Entered the correct MFA token code\n")
    print(err)

finally:
    print("Cleaning up...")

    # Clean up
    if os.path.exists(tempJsonFile):
        json_file.close()
        os.remove(tempJsonFile)
    else:
        print("The file does not exist")

    print("Complete!")
