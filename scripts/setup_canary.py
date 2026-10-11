import json
import zipfile
import io
import time
import boto3

REGION = 'ap-south-1'
CANARY_NAME = 'fcc-uptime-canary'
BUCKET_NAME = 'fcc-cw-canary-319634665438'
ROLE_NAME = 'CloudWatchSyntheticsRole-fcc-uptime-canary'

iam = boto3.client('iam')
synthetics = boto3.client('synthetics', region_name=REGION)

def setup_iam_role():
    trust_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "Service": "lambda.amazonaws.com"
                },
                "Action": "sts:AssumeRole"
            }
        ]
    }

    try:
        role = iam.create_role(
            RoleName=ROLE_NAME,
            AssumeRolePolicyDocument=json.dumps(trust_policy),
            Description='Execution role for CloudWatch Synthetics canary'
        )
        print(f"Created IAM Role: {ROLE_NAME}")
        role_arn = role['Role']['Arn']
    except iam.exceptions.EntityAlreadyExistsException:
        print(f"IAM Role {ROLE_NAME} already exists.")
        role_arn = iam.get_role(RoleName=ROLE_NAME)['Role']['Arn']

    # Attach permissions policy
    policy_doc = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "s3:PutObject",
                    "s3:GetObject"
                ],
                "Resource": [
                    f"arn:aws:s3:::{BUCKET_NAME}/*"
                ]
            },
            {
                "Effect": "Allow",
                "Action": [
                    "s3:GetBucketLocation"
                ],
                "Resource": [
                    f"arn:aws:s3:::{BUCKET_NAME}"
                ]
            },
            {
                "Effect": "Allow",
                "Action": [
                    "logs:CreateLogGroup",
                    "logs:CreateLogStream",
                    "logs:PutLogEvents"
                ],
                "Resource": [
                    "arn:aws:logs:*:*:*"
                ]
            },
            {
                "Effect": "Allow",
                "Action": [
                    "cloudwatch:PutMetricData"
                ],
                "Resource": [
                    "*"
                ],
                "Condition": {
                    "StringEquals": {
                        "cloudwatch:namespace": "CloudWatchSynthetics"
                    }
                }
            }
        ]
    }

    iam.put_role_policy(
        RoleName=ROLE_NAME,
        PolicyName='CloudWatchSyntheticsPolicy',
        PolicyDocument=json.dumps(policy_doc)
    )
    print("Attached CloudWatchSyntheticsPolicy inline policy to role.")
    return role_arn

def create_canary_zip():
    # Standard Node.js Canary script
    node_script = """
const synthetics = require('Synthetics');
const log = require('SyntheticsLogger');

const pageLoadBlueprint = async function () {
    const URL = "http://13.204.82.29/";
    let page = await synthetics.getPage();
    const response = await page.goto(URL, {waitUntil: ['load', 'networkidle0'], timeout: 30000});
    if (!response) {
        throw new Error("Failed to load page: response was null");
    }
    const status = response.status();
    log.info(`Response status code for ${URL}: ${status}`);
    if (status !== 200) {
        throw new Error(`Unexpected status code: ${status}`);
    }
    await synthetics.takeScreenshot('homepage-loaded', 'loaded');
};

exports.handler = async () => {
    return await pageLoadBlueprint();
};
"""
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('nodejs/node_modules/pageLoadBlueprint.js', node_script)
    
    return zip_buffer.getvalue()

def deploy_canary(role_arn):
    zip_bytes = create_canary_zip()
    print("Waiting 10 seconds for IAM Role propagation...")
    time.sleep(10)

    try:
        response = synthetics.create_canary(
            Name=CANARY_NAME,
            Code={
                'ZipFile': zip_bytes,
                'Handler': 'pageLoadBlueprint.handler'
            },
            ArtifactS3Location=f"s3://{BUCKET_NAME}/canary-artifacts",
            ExecutionRoleArn=role_arn,
            Schedule={
                'Expression': 'rate(5 minutes)',
                'DurationInSeconds': 0
            },
            RunConfig={
                'TimeoutInSeconds': 60,
                'MemoryInMB': 960
            },
            SuccessRetentionPeriodInDays=31,
            FailureRetentionPeriodInDays=31,
            RuntimeVersion='syn-nodejs-puppeteer-9.1'
        )
        print("Successfully created Canary:", response['Canary']['Name'])
        print("Starting canary...")
        synthetics.start_canary(Name=CANARY_NAME)
        print("Canary started successfully!")
    except synthetics.exceptions.ConflictException:
        print(f"Canary {CANARY_NAME} already exists.")
    except Exception as e:
        print(f"Canary deployment note: {e}")

if __name__ == '__main__':
    role_arn = setup_iam_role()
    deploy_canary(role_arn)
