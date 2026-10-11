# Cloud Monitoring & Observability Implementation Guide

**Course:** Fundamentals of Cloud Computing  
**Level:** Second-Year B.Tech Course Project  
**Target Environment:** AWS EC2 (Ubuntu 22.04 LTS, Apache2)  
**Live Target Website:** `http://13.204.82.29/`  
**Active AWS Region:** `ap-south-1` (Mumbai)

---

## 📑 Executive Summary & Guide Recommendations Analysis

During project review, course guides often suggest enterprise-grade monitoring mechanisms. Using available AWS Credits, we implemented **real, native AWS cloud monitoring services** without exceeding budget or falsifying architectural tiers:

| Guide Recommendation | Status in Our Project | Native AWS Implementation |
| :--- | :---: | :--- |
| **1. Uptime Checking / Synthetic Monitoring** | **✅ Implemented in AWS** | **AWS CloudWatch Synthetics Canary (`fcc-uptime-canary`)** running Puppeteer headless browser every 5 min + **Route 53 Global Health Check** from 8 global regions + Local CLI script. |
| **2. Real User Monitoring (RUM)** | **✅ Implemented (Client-Side)** | Client-side RUM using W3C **Navigation Timing API** capturing real visitor TTFB and DOM Ready latency without costly Cognito pools. |
| **3. Root Cause Analysis & Alerting** | **✅ Implemented in AWS** | **Amazon SNS Topic (`fcc-monitoring-alerts`)** linked to CloudWatch Metric Alarms (`StatusCheckFailed` & `CPUUtilization`). Apache error logs (`/var/log/apache2/error.log`). |
| **4. Live Executive Dashboard** | **✅ Implemented in AWS** | **CloudWatch Dashboard (`FCC-Web-Hosting-Dashboard`)** with 6 real-time widgets (CPU, Reachability, Network, Alarms, Canary availability). |
| **5. SSL Certificate & Domain CDN** | **🔄 Documented as Phase 2** | AWS CloudFront distributions require an initial account verification ticket for new AWS accounts. Route 53 domain registration is documented under Phase 2 Future Scope. |
| **6. API and Database Monitoring** | **❌ Not Applicable** | Our architecture is a **static web server** served directly by Apache. There is **no backend API** and **no database**. Faking database monitoring would be architecturally inaccurate. |

---

## 🌟 Feature 1: AWS CloudWatch Synthetics Canary (Official AWS Uptime Probe)

We deployed a native AWS CloudWatch Canary powered by AWS Lambda and Puppeteer in Mumbai (`ap-south-1`):

- **Canary Name:** `fcc-uptime-canary`
- **Schedule:** Runs every 5 minutes (`rate(5 minutes)`)
- **Execution Script:** Headless Chromium browser navigates to `http://13.204.82.29/`, validates HTTP 200 OK, measures page load duration, and takes automated visual screenshots.
- **S3 Artifact Bucket:** `s3://fcc-cw-canary-319634665438/canary-artifacts`
- **Saved Evidence:** Stored in project folder at [`screenshots/aws_canary_verified_screenshot.png`](file:///c:/Users/JEETSINGH%20RAJPUT/Downloads/FCC/screenshots/aws_canary_verified_screenshot.png).
- **Console Location:** **AWS Management Console** &rarr; **CloudWatch** &rarr; **Synthetics Canaries** &rarr; click `fcc-uptime-canary`.

---

## 🌍 Feature 2: Amazon Route 53 Global Edge Health Checking

To verify global reachability across worldwide internet backbones, we launched an Amazon Route 53 Health Check:

- **Health Check ID:** `b18efb43-f652-4a6a-9850-ccef8821e4dd`
- **Target:** `13.204.82.29:80` (HTTP `/`)
- **Probing Edge Regions:**
  - `ap-south-1` / `ap-southeast-1` (Singapore)
  - `ap-northeast-1` (Tokyo)
  - `ap-southeast-2` (Sydney)
  - `eu-west-1` (Ireland)
  - `us-east-1` (N. Virginia)
  - `us-west-1` / `us-west-2` (Oregon/California)
  - `sa-east-1` (São Paulo)
- **Status:** **100% HEALTHY (Success: HTTP Status Code 200, OK across all 8 regions)**.
- **Console Location:** **AWS Management Console** &rarr; **Route 53** &rarr; **Health checks**.

---

## 📊 Feature 3: AWS CloudWatch Executive Live Dashboard

A production dashboard has been provisioned directly in your AWS account:

- **Dashboard Name:** `FCC-Web-Hosting-Dashboard`
- **Region:** `ap-south-1` (Mumbai)
- **Console Location:** **AWS Management Console** &rarr; **CloudWatch** &rarr; **Dashboards** &rarr; click `FCC-Web-Hosting-Dashboard`.
- **Integrated Widgets:**
  1. **Header Banner:** Project title, student level (Second Year B.Tech), instance ID (`i-0875444197e8dba94`), public IP (`13.204.82.29`).
  2. **Active Health Alarms:** Real-time status badge of all active CloudWatch alarms.
  3. **CPU Utilization (%):** Time-series graph with red horizontal line marking the 80% alarm threshold.
  4. **System & Instance Reachability Checks:** 2/2 hardware and OS checks graph.
  5. **Network Ingress & Egress Traffic:** Bandwidth volume in bytes.
  6. **Synthetics Canary Availability (%):** 24/7 uptime percentage calculated by AWS.
  7. **Page Load Duration (ms):** End-to-end user load latency measured by AWS Lambda headless browser.

---

## 🔔 Feature 4: CloudWatch Alarms & Amazon SNS Email Notifications

### Configured Alarms
1. **`fcc-web-server-status-check-failed`**:
   - Metric: `StatusCheckFailed` on `i-0875444197e8dba94`
   - Condition: `>= 1`
   - Action: Publishes to `arn:aws:sns:ap-south-1:319634665438:fcc-monitoring-alerts`
2. **`HighCPUUtilization-fcc-web-server`**:
   - Metric: `CPUUtilization` on `i-0875444197e8dba94`
   - Condition: `> 80%` for 5 minutes
   - Action: Publishes to `arn:aws:sns:ap-south-1:319634665438:fcc-monitoring-alerts`

### How to Subscribe Your Email to the SNS Topic
Run this single command in terminal with your email address:
```bash
aws sns subscribe --topic-arn "arn:aws:sns:ap-south-1:319634665438:fcc-monitoring-alerts" --protocol email --notification-endpoint "YOUR_EMAIL@gmail.com" --region ap-south-1
```
*Then open your inbox and click "Confirm subscription" in the email from AWS.*

### How to Test an Alarm Email During Faculty Demo
To demonstrate the alarm triggering and email arriving live to your phone/laptop:
```bash
# Force alarm state into ALARM
aws cloudwatch set-alarm-state --alarm-name "fcc-web-server-status-check-failed" --state-value ALARM --state-reason "Faculty Viva Demonstration" --region ap-south-1

# Reset alarm back to OK
aws cloudwatch set-alarm-state --alarm-name "fcc-web-server-status-check-failed" --state-value OK --state-reason "Restored normal operation" --region ap-south-1
```

---

## 💻 Feature 5: Local Synthetic Uptime CLI Suite

For quick local testing and CSV audit trail generation:
```bash
# Python Cross-Platform Monitor
python scripts/uptime_monitor.py --count 5 --interval 2

# PowerShell Monitor
powershell -ExecutionPolicy Bypass -File scripts\UptimeMonitor.ps1 -MaxChecks 5
```

---

## 🎯 Viva & Faculty Defense Questions

**Q1: How do you know the website is accessible from other countries?**  
> *"We configured an Amazon Route 53 Global Health Check (`b18efb43-f652-4a6a-9850-ccef8821e4dd`). Probing nodes from Singapore, Tokyo, Sydney, Ireland, Virginia, California, and São Paulo probe our EC2 Public IP every 30 seconds, confirming HTTP 200 OK globally."*

**Q2: What is the difference between CloudWatch Metrics and CloudWatch Synthetics?**  
> *"CloudWatch Metrics capture server infrastructure statistics (like CPU and network traffic from the hypervisor). CloudWatch Synthetics (`fcc-uptime-canary`) launches a headless browser every 5 minutes from AWS to simulate a real user visiting the website, testing end-to-end HTTP response, capturing DOM render time, and storing screenshots in S3."*

**Q3: How are alerts routed when a failure happens?**  
> *"We created an Amazon SNS Topic (`fcc-monitoring-alerts`) subscribed to CloudWatch metric alarms for `StatusCheckFailed` and `CPUUtilization`. If the server fails or CPU exceeds 80%, CloudWatch publishes a notification to SNS, which dispatches an email directly to the registered administrator address."*

**Q4: Where can we view all these metrics in one place?**  
> *"In the AWS Management Console under CloudWatch Dashboards, we created `FCC-Web-Hosting-Dashboard`. It provides an executive single-pane view showing real-time CPU, Reachability checks, Network throughput, active alarms, and Synthetic Canary uptime percentages."*
