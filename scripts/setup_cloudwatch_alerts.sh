#!/usr/bin/env bash
# ==============================================================================
# Project: Cloud-Based Website Hosting and Monitoring System Using AWS
# Course: Fundamentals of Cloud Computing (Second-Year B.Tech)
# Script: setup_cloudwatch_alerts.sh
# Purpose: Configure Amazon CloudWatch Alarms & Amazon SNS Email Notifications
# ==============================================================================

set -euo pipefail

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}==================================================================${NC}"
echo -e "${BLUE}  AWS CloudWatch & SNS Alerting Configuration Setup               ${NC}"
echo -e "${BLUE}  Course: Fundamentals of Cloud Computing (Second-Year B.Tech)   ${NC}"
echo -e "${BLUE}==================================================================${NC}"

# Variables (Customizable for your AWS account & EC2 Instance)
AWS_REGION="${AWS_REGION:-ap-south-1}"
TOPIC_NAME="fcc-monitoring-alerts"

# Prompt or use environment variable for instance ID & email
INSTANCE_ID="${1:-}"
ALERT_EMAIL="${2:-}"

if [ -z "$INSTANCE_ID" ]; then
    echo -e "${YELLOW}Notice: Instance ID not passed as argument.${NC}"
    # Try fetching instance metadata if running directly on EC2
    INSTANCE_ID=$(curl -s --connect-timeout 2 http://169.254.169.254/latest/meta-data/instance-id 2>/dev/null || echo "")
fi

if [ -z "$INSTANCE_ID" ]; then
    echo -e "Usage: ./setup_cloudwatch_alerts.sh <INSTANCE_ID> <YOUR_EMAIL>"
    echo -e "Example: ./setup_cloudwatch_alerts.sh i-0a1b2c3d4e5f6g7h student@example.com"
    exit 1
fi

if [ -z "$ALERT_EMAIL" ]; then
    echo -e "${RED}[ERROR] Please provide your email address to receive alert notifications.${NC}"
    echo -e "Example: ./setup_cloudwatch_alerts.sh $INSTANCE_ID student@example.com"
    exit 1
fi

echo -e "\nTarget EC2 Instance : ${GREEN}${INSTANCE_ID}${NC}"
echo -e "Notification Email  : ${GREEN}${ALERT_EMAIL}${NC}"
echo -e "AWS Region          : ${GREEN}${AWS_REGION}${NC}"

# Step 1: Create Amazon SNS Topic
echo -e "\n${YELLOW}[Step 1/4] Creating Amazon SNS Topic: ${TOPIC_NAME}...${NC}"
TOPIC_ARN=$(aws sns create-topic --name "${TOPIC_NAME}" --region "${AWS_REGION}" --query "TopicArn" --output text)
echo -e "${GREEN}[OK] SNS Topic created with ARN:${NC} ${TOPIC_ARN}"

# Step 2: Subscribe Email to SNS Topic
echo -e "\n${YELLOW}[Step 2/4] Subscribing email ${ALERT_EMAIL} to SNS Topic...${NC}"
SUBSCRIPTION_ARN=$(aws sns subscribe \
    --topic-arn "${TOPIC_ARN}" \
    --protocol email \
    --notification-endpoint "${ALERT_EMAIL}" \
    --region "${AWS_REGION}" \
    --query "SubscriptionArn" --output text)
echo -e "${GREEN}[OK] Subscription initiated. Status: ${SUBSCRIPTION_ARN}${NC}"
echo -e "${YELLOW}>> CHECK YOUR INBOX: AWS has sent a confirmation email to ${ALERT_EMAIL}.${NC}"
echo -e "${YELLOW}>> You MUST click 'Confirm subscription' in that email to receive alerts.${NC}"

# Step 3: Create CloudWatch Alarm for EC2 Status Check Failures (Downtime / Hardware Failure)
echo -e "\n${YELLOW}[Step 3/4] Configuring CloudWatch Alarm: EC2-StatusCheckFailed...${NC}"
aws cloudwatch put-metric-alarm \
    --alarm-name "fcc-web-server-status-check-failed" \
    --alarm-description "Triggers alarm and sends email if EC2 instance status check fails for 1 period" \
    --metric-name "StatusCheckFailed" \
    --namespace "AWS/EC2" \
    --statistic "Maximum" \
    --period 60 \
    --evaluation-periods 1 \
    --threshold 1 \
    --comparison-operator "GreaterThanOrEqualToThreshold" \
    --dimensions Name=InstanceId,Value="${INSTANCE_ID}" \
    --alarm-actions "${TOPIC_ARN}" \
    --ok-actions "${TOPIC_ARN}" \
    --region "${AWS_REGION}"
echo -e "${GREEN}[OK] StatusCheckFailed alarm configured successfully.${NC}"

# Step 4: Create / Update CloudWatch Alarm for High CPU Utilization
echo -e "\n${YELLOW}[Step 4/4] Configuring CloudWatch Alarm: High CPU Utilization (>80%)...${NC}"
aws cloudwatch put-metric-alarm \
    --alarm-name "fcc-web-server-high-cpu" \
    --alarm-description "Triggers alarm and sends email if CPU exceeds 80% for 5 minutes" \
    --metric-name "CPUUtilization" \
    --namespace "AWS/EC2" \
    --statistic "Average" \
    --period 300 \
    --evaluation-periods 1 \
    --threshold 80 \
    --comparison-operator "GreaterThanThreshold" \
    --dimensions Name=InstanceId,Value="${INSTANCE_ID}" \
    --alarm-actions "${TOPIC_ARN}" \
    --ok-actions "${TOPIC_ARN}" \
    --region "${AWS_REGION}"
echo -e "${GREEN}[OK] High CPU alarm configured successfully.${NC}"

echo -e "\n${BLUE}==================================================================${NC}"
echo -e "${GREEN}  CLOUDWATCH & SNS MONITORING CONFIGURATION COMPLETE!             ${NC}"
echo -e "${BLUE}==================================================================${NC}"
echo -e "To test sending an instant demo alarm email to your inbox, run:"
echo -e "  aws cloudwatch set-alarm-state --alarm-name fcc-web-server-status-check-failed --state-value ALARM --state-reason \"Faculty demo test\" --region ${AWS_REGION}"
echo -e "\nTo reset the alarm back to OK:"
echo -e "  aws cloudwatch set-alarm-state --alarm-name fcc-web-server-status-check-failed --state-value OK --state-reason \"Restored normal operation\" --region ${AWS_REGION}"
echo -e "${BLUE}==================================================================${NC}\n"
