# 🎬 Faculty Demo Walkthrough Script

**Project Title:** Cloud-Based Website Hosting and Monitoring System Using AWS  
**Course:** Fundamentals of Cloud Computing  
**Level:** Second-Year B.Tech Course Project  
**Student Name:** Jeet Singh Rajput  
**Target Environment:** AWS EC2 (Ubuntu 22.04 LTS, Apache2)  
**Live Target Website:** `http://13.204.82.29/`  
**AWS Region:** `ap-south-1` (Mumbai)

---

## 📋 Pre-Demo Checklist (Open These 5 Tabs Before Your Faculty Arrives)

Before calling your faculty or course guide to your screen, open these tabs in your browser:

1. **Tab 1: Live Public Website**  
   👉 URL: `http://13.204.82.29/`
2. **Tab 2: AWS CloudWatch Executive Dashboard**  
   👉 AWS Console &rarr; CloudWatch &rarr; Dashboards &rarr; **`FCC-Web-Hosting-Dashboard`**
3. **Tab 3: AWS CloudWatch Synthetics Canaries**  
   👉 AWS Console &rarr; CloudWatch &rarr; Synthetics Canaries &rarr; **`fcc-uptime-canary`**
4. **Tab 4: Amazon Route 53 Global Health Checks**  
   👉 AWS Console &rarr; Route 53 &rarr; **Health checks** (`b18efb43-f652-4a6a-9850-ccef8821e4dd`)
5. **Tab 5: Your Email Inbox**  
   👉 Have your inbox open with the recent emails from **AWS Notifications** (`ALARM` and `OK` recovery).
6. **Terminal / PowerShell**  
   👉 Open PowerShell in `FCC/` directory ready to run scripts.

---

## 🎙️ Step-by-Step Demonstration Script (5 to 7 Minutes)

### Step 1: Introduction & Project Overview (30 to 45 Seconds)

**What you do:** Stand by your screen with Tab 1 open.  
**What you say:**
> *"Good morning/afternoon, Sir/Ma'am. Today, I am demonstrating my Fundamentals of Cloud Computing course project: **'Cloud-Based Website Hosting and Monitoring System Using AWS'**.*  
> 
> *In traditional computing, hosting a website on a local machine suffers from single points of failure, lack of high availability, and zero health visibility. In this project, I provisioned an **Ubuntu EC2 virtual server (`t3.micro`)** running the **Apache HTTP Server** in AWS Mumbai (`ap-south-1`), secured by AWS Security Groups and IAM.*  
> 
> *Based on your recommendations, I went beyond basic hosting and implemented a complete **multi-tier cloud observability and monitoring architecture** including **CloudWatch Dashboards**, **Amazon Route 53 Global Health Probes**, **AWS Synthetics Headless Browser Canaries**, and an **Amazon SNS automated email alerting pipeline**."*

---

### Step 2: Demonstrating the Live Website & Client-Side RUM (1 to 2 Minutes)

**What you do:** Switch to **Tab 1** (`http://13.204.82.29/`).  
**What you say:**
> *"Here is the live website accessible to the public over IPv4 at `http://13.204.82.29/`. The website presents our cloud architecture, technology stack, and interactive telemetry.*  
> 
> *Regarding **Real User Monitoring (RUM)**: Enterprise AWS CloudWatch RUM requires Amazon Cognito Identity Pools and incurs per-session fees. To implement RUM cleanly without unnecessary costs, I integrated the **W3C Navigation Timing API** directly into our frontend JavaScript (`app.js`).*  
> 
> *If you look at the **Live Telemetry Terminal** right here on the homepage, whenever a real visitor opens this page, it measures the exact **Client TTFB (Time to First Byte)** and **DOM Ready Latency**."*

**Interactive Action:**
1. Click the **"Live Telemetry"** tab in the navbar (or scroll just below the hero fold between Home and About) to the **Live CloudWatch Telemetry Simulator**.
2. Click the orange **"Simulate Traffic Spike"** button.
3. Show the gauge jump into red (`ALARM: CPU > 80%`), log elevated traffic, and announce that Amazon SNS has dispatched an alert email.
4. Watch it automatically cool down back to normal green (`OK`) after 7 seconds.

---

### Step 3: Demonstrating the AWS CloudWatch Executive Dashboard (1.5 Minutes)

**What you do:** Switch to **Tab 2** (CloudWatch &rarr; `FCC-Web-Hosting-Dashboard`).  
**What you say:**
> *"Now let's view the actual AWS cloud infrastructure in the AWS Management Console. I created a centralized executive dashboard called **`FCC-Web-Hosting-Dashboard`**.*  
> 
> *It gives us real-time visibility through 6 distinct widgets:*
> 1. *🚨 **Active Alarms Widget:** Shows the current health state of our alarms.*
> 2. *⚡ **CPU Utilization (%):** Real-time EC2 processor load with a red horizontal annotation line at our 80% alarm threshold.*
> 3. *🩺 **Reachability Checks:** Tracks hypervisor and virtual OS status checks ($2/2$ passed).*
> 4. *🌐 **Network Ingress & Egress:** Inbound and outbound network bandwidth in bytes.*
> 5. *🔍 **Canary Availability (%):** Continuous 24/7 uptime percentage calculated by AWS.*
> 6. *⏱️ **Page Load Duration:** Real-time end-to-end page render duration in milliseconds."*

---

### Step 4: Demonstrating Synthetic Uptime Monitoring (1.5 Minutes)

**What you do:** Switch to **Tab 3** (Synthetics Canaries &rarr; `fcc-uptime-canary`) and **Tab 4** (Route 53).  
**What you say:**
> *"For **Synthetic Monitoring**, internal server metrics aren't enough because a server might have low CPU while Apache is crashed. Therefore, I implemented two layers of external synthetic testing:*
> 
> *1. **AWS CloudWatch Synthetics Canary (`fcc-uptime-canary`):**  
> *AWS launches a serverless Lambda function running a **headless Chromium browser (Puppeteer)** every 5 minutes in Mumbai. It loads `http://13.204.82.29/`, verifies HTTP 200 OK, captures page load latency, and automatically takes visual screenshots stored in Amazon S3.* *(Show the 100% pass rate graph and screenshot tab in the console).*  
> 
> *2. **Amazon Route 53 Global Edge Health Checks:**  
> *(Switch to Tab 4)*  
> *Route 53 health checkers in **8 worldwide AWS regions** (Tokyo, Singapore, Sydney, Ireland, Virginia, Oregon, California, São Paulo) probe our web server every 30 seconds. As you can see, all 8 regions report **100% Healthy (HTTP 200 OK)**."*

**CLI Bonus Demo:**
Switch to PowerShell and run the Python monitor:
```bash
python scripts/uptime_monitor.py --count 3 --interval 1
```
> *"We also created a local automated CLI monitor that logs every probe to `uptime_log.csv` for audit reporting."*

---

### Step 5: Demonstrating the Automated SNS Email Alerting Pipeline (1 Minute)

**What you do:** Switch to **Tab 5** (Email Inbox).  
**What you say:**
> *"For **Root Cause Analysis & Alerting**, we connected our CloudWatch alarms to an **Amazon SNS Topic (`fcc-monitoring-alerts`)**.*  
> 
> *Whenever `StatusCheckFailed` exceeds 1 or CPU exceeds 80%, CloudWatch publishes to SNS, which dispatches an email alert to the system administrator.*  
> 
> *Crucially, we also configured **OKActions** so when the system recovers, it sends an automatic **OK Recovery Email**.*  
> *(Show the real emails from AWS Notifications in your inbox: one showing ALARM and one showing OK recovery).*  
> 
> *If an outage occurs, root cause analysis is performed on the server by inspecting `/var/log/apache2/error.log` and `journalctl -u apache2`."*

---

### Step 6: Conclusion (30 Seconds)

**What you say:**
> *"To conclude, this project satisfies all second-year cloud computing curriculum requirements: Infrastructure-as-a-Service (EC2), Linux server administration, web server deployment (Apache), cloud security (Security Groups & IAM), and an enterprise-grade multi-tier monitoring suite (CloudWatch, Route 53, Synthetics, and SNS). Thank you, and I am happy to answer any questions."*

---

## ❓ Faculty Viva & Defense Q&A Cheat Sheet

| Question | Winning Answer to Give |
| :--- | :--- |
| **Q: Why didn't you monitor a database?** | *"Our application is architected as a high-performance **static website** delivered directly by Apache from `/var/www/html/`. Because there is no backend API microservice or database (like RDS MySQL), monitoring non-existent databases would be architecturally inaccurate."* |
| **Q: Why is HTTPS / SSL not enabled?** | *"SSL certificates require a verified Fully Qualified Domain Name (FQDN) mapped through DNS (like Route 53). Because we are hosting directly on an EC2 Public IPv4 to stay within the zero-cost AWS Free Tier / starter credit scope, domain registration and SSL certificates are documented in our **Phase 2 Future Scope**."* |
| **Q: What is the difference between CloudWatch Metrics and Synthetics?** | *"CloudWatch Metrics capture internal virtual machine resource usage (CPU, Network, disk). Synthetics Canaries simulate a real external user opening the web page in a browser from the internet to verify that the web application actually works and renders."* |
| **Q: How much does this monitoring setup cost?** | *"The CloudWatch Dashboard is 100% free (AWS includes 3 free dashboards). Amazon SNS includes 1,000 free emails/month. Route 53 Health Checks cost ~$0.50/month and CloudWatch Synthetics costs ~$1.20/month. The entire setup costs less than $2.00/month, fully covered by our AWS Credits."* |
