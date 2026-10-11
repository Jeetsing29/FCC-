# Deploy S3 with AWS CLI

This document shows a simple beginner-friendly workflow for deploying the static website in the `website/` folder to an Amazon S3 bucket.

## AWS CLI Commands

Check the AWS CLI version:

```bash
aws --version
```

Configure AWS credentials locally:

```bash
aws configure
```

Verify the active AWS identity:

```bash
aws sts get-caller-identity
```

List available S3 buckets:

```bash
aws s3 ls
```

Deploy the website files to your S3 bucket:

```bash
aws s3 sync website/ s3://YOUR_BUCKET_NAME --delete
```

## Screenshot

AWS CLI deployment example:

![AWS CLI deployment screenshot](../screenshots/lab02-aws-cli-deployment.png)

## Safety Notes

- Do not share or commit AWS credentials to GitHub
- Double-check the AWS account before uploading files
- Make sure `YOUR_BUCKET_NAME` is replaced with the correct bucket
- Review the `--delete` flag carefully because it removes files in the bucket that are not present in the local `website/` folder
- Keep the deployment limited to the static website files only
- Delete or clean up resources that are no longer needed to reduce unnecessary cost
