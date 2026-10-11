# Cost Control Checklist

This checklist is intended for a beginner AWS learning environment. The goal is to reduce unnecessary cost and avoid common mistakes during hands-on lab practice.

## Budget Setup

- Create an AWS Budget before starting multiple labs
- Set a low monthly threshold that fits a personal learning project
- Enable email alerts so unexpected usage is noticed early

## Free Tier Awareness

- Check whether the services used in the lab are covered by the AWS Free Tier
- Remember that Free Tier limits can still be exceeded
- Review region, storage, and usage details before leaving resources running

## EC2 Termination

- Stop EC2 instances when they are not actively being used
- Terminate practice instances after finishing the lab if they are no longer needed
- Remove unused volumes or related resources if they were created during testing

## No Access Keys in GitHub

- Never commit AWS access keys, secret keys, or CLI credential files to GitHub
- Add sensitive local files to `.gitignore` if needed
- Rotate credentials immediately if they are exposed by mistake

## No Sensitive Data in Public S3 Bucket

- Keep public S3 bucket content limited to static website files only
- Do not upload personal documents, credentials, or private datasets
- Review bucket contents before enabling public website access

## Check Active Resources After Each Lab

- Review running EC2 instances
- Review S3 buckets and stored objects
- Review CloudWatch alarms created for practice
- Review AWS Budgets configuration
- Remove or clean up anything that is no longer part of the lab
