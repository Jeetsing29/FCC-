import json
import boto3

def deploy_dashboard():
    cw = boto3.client('cloudwatch', region_name='ap-south-1')
    with open('scripts/dashboard_config.json', 'r', encoding='utf-8') as f:
        body = f.read()

    response = cw.put_dashboard(
        DashboardName='FCC-Web-Hosting-Dashboard',
        DashboardBody=body
    )
    print("Dashboard deployment response:", response)

if __name__ == '__main__':
    deploy_dashboard()
