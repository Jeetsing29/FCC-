import time
import boto3

def create_distribution():
    cf = boto3.client('cloudfront')
    caller_ref = f"fcc-web-server-cf-{int(time.time())}"
    
    origin_domain = "ec2-13-204-82-29.ap-south-1.compute.amazonaws.com"
    origin_id = "EC2-Apache-Origin"

    distribution_config = {
        'CallerReference': caller_ref,
        'Comment': 'FCC Web Hosting System CDN with SSL HTTPS',
        'Enabled': True,
        'Origins': {
            'Quantity': 1,
            'Items': [
                {
                    'Id': origin_id,
                    'DomainName': origin_domain,
                    'CustomOriginConfig': {
                        'HTTPPort': 80,
                        'HTTPSPort': 443,
                        'OriginProtocolPolicy': 'http-only',
                        'OriginSslProtocols': {
                            'Quantity': 1,
                            'Items': ['TLSv1.2']
                        },
                        'OriginReadTimeout': 30,
                        'OriginKeepaliveTimeout': 5
                    }
                }
            ]
        },
        'DefaultCacheBehavior': {
            'TargetOriginId': origin_id,
            'ViewerProtocolPolicy': 'redirect-to-https',
            'AllowedMethods': {
                'Quantity': 2,
                'Items': ['GET', 'HEAD'],
                'CachedMethods': {
                    'Quantity': 2,
                    'Items': ['GET', 'HEAD']
                }
            },
            'ForwardedValues': {
                'QueryString': False,
                'Cookies': {'Forward': 'none'}
            },
            'MinTTL': 0,
            'DefaultTTL': 3600,
            'MaxTTL': 86400,
            'Compress': True
        }
    }

    print("Submitting CloudFront distribution creation request...")
    response = cf.create_distribution(DistributionConfig=distribution_config)
    dist = response['Distribution']
    print("SUCCESS: CloudFront Distribution Created!")
    print(f"Distribution ID  : {dist['Id']}")
    print(f"Domain Name      : https://{dist['DomainName']}/")
    print(f"Status           : {dist['Status']}")
    return dist

if __name__ == '__main__':
    create_distribution()
