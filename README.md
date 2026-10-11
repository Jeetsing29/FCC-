# Cloud-Based Website Hosting and Monitoring System Using AWS

**Course:** Fundamentals of Cloud Computing  
**Level:** Second-Year B.Tech Course Project  
**Project Title:** Cloud-Based Website Hosting and Monitoring System Using AWS  

---

## 📌 Introduction

In traditional computing, websites were hosted on local physical computers or on-premise servers. If the computer lost power or disconnected from the internet, the website would go down. 

Cloud computing solves this problem by allowing us to rent computing power, storage, and networking over the internet from providers like **Amazon Web Services (AWS)**. 

This project is a beginner-level practical demonstration created for the **Fundamentals of Cloud Computing** course. It demonstrates how to host a lightweight, responsive website on a cloud virtual server using **Amazon EC2**, serve it to the public using the **Apache HTTP Server**, manage assets with **Amazon S3**, enforce security using **AWS IAM**, and monitor server health in real time using **Amazon CloudWatch**.

---

## ❓ Problem Statement

Running web applications on local computers has several limitations:
1. **Lack of High Availability:** A website hosted on a personal laptop stops working whenever the laptop is closed, restarted, or disconnected from Wi-Fi.
2. **No Public Accessibility:** Local development servers (like `localhost:8000`) cannot be accessed by outside users without complex networking or router port forwarding.
3. **No Health Visibility:** If a local server runs out of memory or crashes, there is no automatic system to track the problem or send an alert.
4. **Security Risks:** Exposing personal computers directly to the public internet creates major security risks without firewall rules and access control.

**The Solution:** Deploying the website to an AWS cloud environment using an Ubuntu EC2 virtual instance protected by AWS Security Groups, administered through SSH, and monitored by Amazon CloudWatch.

---

## 🎯 Objectives

The main goals of this project are:
- To launch and configure a virtual cloud server on **AWS EC2** running Ubuntu Linux.
- To install, configure, and manage the **Apache HTTP Server (`apache2`)** to serve website files on port 80.
- To configure an **AWS Security Group** as a virtual firewall allowing authorized HTTP and SSH traffic.
- To understand object storage by organizing static files and project assets with **Amazon S3**.
- To follow cloud security best practices using **AWS IAM** and the principle of least privilege.
- To monitor virtual server health (CPU utilization and status checks) using **Amazon CloudWatch**.
- To administer a remote Linux machine using command-line tools over secure **SSH**.
- To practice software version control using **Git and GitHub**.

---

## 🛠️ Technologies Used

| Technology | Category | Description |
| :--- | :--- | :--- |
| **HTML5** | Frontend Structure | Provides the semantic structure and content of the website. |
| **CSS3** | Frontend Styling | Modern styling with an AWS dark theme, responsive grids, and clean layout. |
| **Vanilla JavaScript** | Frontend Interactivity | Handles mobile navigation and an interactive live telemetry simulator. |
| **Ubuntu Linux (22.04 LTS)** | Operating System | Open-source Linux distribution running on the EC2 virtual server. |
| **Apache HTTP Server (`apache2`)** | Web Server | Production web server that listens for incoming HTTP requests on port 80. |
| **SSH (Secure Shell)** | Remote Administration | Encrypted network protocol for secure remote command-line login. |
| **Bash (`deploy.sh`)** | Automation Script | Shell script that automates package installation, file copying, and service restart. |
| **Git & GitHub** | Version Control | Tracks source code revisions and provides remote repository backup. |
| **Python 3** | Local Testing | Uses `http.server` module for testing the website locally before cloud deployment. |

---

## ☁️ AWS Services Used

1. **Amazon EC2 (Elastic Compute Cloud):**
   - Provides scalable virtual computing capacity in the cloud.
   - We use an EC2 `t3.micro` instance (2 vCPU, 1 GiB Memory) in Mumbai (`ap-south-1`) region (`i-0875444197e8dba94`).
   - Runs Ubuntu Linux 22.04 LTS and hosts the production Apache web server.

2. **Amazon S3 (Simple Storage Service):**
   - High-durability cloud object storage.
   - Stores static website assets, project documentation, and AWS CloudWatch Synthetics canary screenshots/artifacts (`s3://fcc-cw-canary-319634665438/`).

3. **Amazon CloudWatch & Synthetics:**
   - Observability, metric collection, and headless browser synthetic monitoring.
   - Features:
     - `CPUUtilization` & `StatusCheckFailed` real-time metric tracking.
     - `FCC-Web-Hosting-Dashboard`: Central executive dashboard with 6 visual widgets.
     - `fcc-uptime-canary`: Headless Chromium browser (Puppeteer) probing `http://13.204.82.29/` every 5 minutes.

4. **Amazon Route 53 (Global Health Checks):**
   - Highly available Domain Name System (DNS) and global health checking service.
   - Active Health Check (`b18efb43-f652-4a6a-9850-ccef8821e4dd`) probing website reachability across 8 worldwide AWS regions every 30 seconds (100% Healthy).

5. **Amazon SNS (Simple Notification Service):**
   - Managed pub/sub push notification service.
   - Topic `fcc-monitoring-alerts` delivers instant email notifications on alarm transitions (`ALARM` and `OK` recovery).

6. **AWS IAM (Identity and Access Management):**
   - Manages users, credentials, and access permissions using the principle of least privilege.

7. **AWS Budgets:**
   - Simple cost-management tool keeping usage within Free Tier and credit limits.

---

## 🏗️ System Architecture

The following diagram illustrates how user requests, synthetic probes, and alerting flows travel through the AWS infrastructure:

```text
       [ External Client Browser ]       [ Route 53 Global Probes ]
                    │                                │ (8 Regions Worldwide)
                    ▼ (HTTP Port 80)                 ▼
               [ Internet ] ◄──────────── [ CloudWatch Synthetics Canary ]
                    │                     (Puppeteer Headless Browser)
                    ▼ (Public IPv4: 13.204.82.29)
    ┌──────────────────────────────────────────────────────────────────┐
    │                        AWS Cloud VPC                             │
    │                                                                  │
    │   ┌──────────────────────────────────────────────────────────┐   │
    │   │               EC2 Security Group (Firewall)              │   │
    │   │   - Inbound Port 80 (HTTP) from 0.0.0.0/0                │   │
    │   │   - Inbound Port 22 (SSH)  from Admin IP                 │   │
    │   └─────────────────────────────┬────────────────────────────┘   │
    │                                 │                                │
    │                                 ▼                                │
    │   ┌──────────────────────────────────────────────────────────┐   │
    │   │              Amazon EC2 Virtual Instance                 │   │
    │   │         (Ubuntu 22.04 LTS - t3.micro - Mumbai)           │   │
    │   │                                                          │   │
    │   │   ┌──────────────────────────────────────────────────┐   │   │
    │   │   │           Apache HTTP Server (apache2)           │   │   │
    │   │   │           Document Root: /var/www/html/          │   │   │
    │   │   └─────────────────────────┬────────────────────────┘   │   │
    │   │                             │                            │   │
    │   │                             ▼                            │   │
    │   │                 [ Website HTML/CSS/JS Files ]            │   │
    │   └─────────────────────────────┬────────────────────────────┘   │
    └─────────────────────────────────┼────────────────────────────────┘
                                      │
            ┌─────────────────────────┼─────────────────────────┐
            ▼                         ▼                         ▼
   ┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
   │    Amazon S3    │       │ Amazon CloudWatch│       │   Amazon SNS    │
   │ (Canary & Assets│       │(Executive Board)│       │  (Email Alerts) │
   └─────────────────┘       └────────┬────────┘       └────────┬────────┘
                                      │                         │
                                      └───────► Alarm Trigger ──┘
                                                    │
                                                    ▼
                                           [ Administrator Inbox ]
```

### Flow Explanation:
1. The **User** types the EC2 Public IP address `http://13.204.82.29/` into their web browser.
2. The request passes across the **Internet** and reaches the AWS network.
3. The **EC2 Security Group** inspects the traffic and permits incoming packets on **Port 80 (HTTP)**.
4. Inside the EC2 instance, the **Apache web server** receives the request and reads the files located in `/var/www/html/`.
5. The client browser executes client-side **Navigation Timing API** telemetry in `app.js` to measure TTFB and DOM ready speed.
6. In parallel, **Route 53 Global Health Checks** (from 8 countries) and **CloudWatch Synthetics Canary** (Puppeteer) continuously test HTTP 200 availability.
7. The **CloudWatch Dashboard** aggregates live CPU, reachability, and canary availability.
8. If thresholds are breached or restored, **Amazon SNS** automatically dispatches email notifications to the administrator.

---

## 🔄 How the Project Works

1. **Step 1 - Local Development:** The website is created using clean HTML, modern CSS, and vanilla JavaScript.
2. **Step 2 - Version Control:** The project files are tracked using Git and uploaded to GitHub.
3. **Step 3 - Cloud Provisioning:** An EC2 virtual server is launched in the AWS Console with an Ubuntu operating system and an attached Security Group.
4. **Step 4 - Remote Server Setup:** The administrator connects to the server using an SSH key pair (`.pem` file) from a local terminal.
5. **Step 5 - Automated Web Deployment:** The `deploy.sh` script runs on the EC2 server to install Apache, copy website files into `/var/www/html/`, and start the web service.
6. **Step 6 - Public Access:** Anyone with the EC2 Public IPv4 address can view the website in their browser.
7. **Step 7 - System Monitoring:** AWS CloudWatch continuously tracks CPU usage and server status to ensure the website stays healthy.

---

## 💻 Local Setup (Testing Before Deployment)

You can test and demonstrate the project locally on your laptop without an AWS account:

### Option 1: Using Python's Built-in HTTP Server (Recommended)
1. Open PowerShell or Command Prompt.
2. Move into the `website` directory:
   ```bash
   cd "website"
   ```
3. Start the local server:
   ```bash
   python -m http.server 8000
   ```
4. Open your browser and visit:
   ```text
   http://localhost:8000
   ```

### Option 2: Direct File Open
Double-click `website/index.html` in your file explorer. It will open directly in Google Chrome, Microsoft Edge, or Mozilla Firefox.

---

## 🚀 AWS EC2 Deployment Steps

Follow these simple steps to deploy the website onto a real AWS EC2 instance.

### Step 1: Launch the EC2 Instance
1. Log in to the [AWS Management Console](https://console.aws.amazon.com/).
2. In the search bar, type **EC2** and click **EC2**.
3. Click the orange **Launch instance** button.
4. Fill in the following basic settings:
   - **Name:** `fcc-web-server`
   - **AMI (Amazon Machine Image):** Select **Ubuntu** (`Ubuntu Server 22.04 LTS` or `24.04 LTS`).
   - **Architecture:** `64-bit (x86)`.
   - **Instance type:** Select `t3.micro` (Free Tier eligible in Mumbai `ap-south-1`).
5. **Key pair (login):**
   - Click **Create new key pair**.
   - Name: `fcc-ec2-key`.
   - Key pair type: **RSA**.
   - Private key file format: **.pem**.
   - Click **Create key pair** and save the downloaded `fcc-ec2-key.pem` file on your computer.

---

### Step 2: Configure the Security Group (Open HTTP Port 80)
Under **Network settings**:
1. Choose **Create security group**.
2. Make sure the following two **Inbound Rules** are checked:
   - **Allow SSH traffic from:** Select `My IP` (or `Anywhere 0.0.0.0/0`).
   - **Allow HTTP traffic from the internet:** Check this box (sets port `80` from `0.0.0.0/0`).
3. Click **Launch instance**.

> [!IMPORTANT]
> If **HTTP (Port 80)** is not allowed in your Security Group, external web browsers will be blocked and your website will fail to load!

---

### Step 3: Connect to EC2 via SSH
Once your instance state shows **Running**:
1. Copy its **Public IPv4 address** from the EC2 instance summary (e.g., `13.204.82.29`).
2. Open PowerShell or Terminal on your computer.
3. If using Linux/macOS, set read-only permissions on your key:
   ```bash
   chmod 400 fcc-ec2-key.pem
   ```
4. Connect to the EC2 instance:
   ```bash
   ssh -i "path/to/fcc-ec2-key.pem" ubuntu@<YOUR-EC2-PUBLIC-IP>
   ```
5. Type `yes` when asked to confirm the host authenticity.

---

### Step 4: Transfer Project Files to EC2
Inside your EC2 terminal session, download the project from GitHub:
```bash
git clone https://github.com/moPPingg/aws-cloud-foundation-project.git
cd aws-cloud-foundation-project
```

---

### Step 5: Run the Automated Deployment Script (`deploy.sh`)
Execute the included deployment script:
```bash
# Make script executable
chmod +x deploy.sh

# Run the deployment
./deploy.sh
```

**What `deploy.sh` does automatically:**
- Updates Ubuntu software package lists (`sudo apt-get update -y`).
- Installs Apache (`apache2`) if it is not already installed.
- Copies all website files to `/var/www/html/`.
- Sets standard web ownership (`www-data:www-data`) and permissions (`755`).
- Enables and restarts the Apache service.
- Performs a local health check and prints your public website URL.

---

### Alternative: Manual Deployment Commands
If you want to run the commands manually for your project evaluation:
```bash
# 1. Update package list
sudo apt update -y

# 2. Install Apache web server
sudo apt install apache2 -y

# 3. Enable Apache to auto-start on boot
sudo systemctl enable apache2

# 4. Copy website files into web root
sudo cp -r website/* /var/www/html/

# 5. Set proper file permissions
sudo chown -R www-data:www-data /var/www/html
sudo chmod -R 755 /var/www/html

# 6. Restart Apache service
sudo systemctl restart apache2

# 7. Check service status
sudo systemctl status apache2
```

---

### Step 6: Access the Live Website in Your Browser
1. In the AWS EC2 Console, find your instance's **Public IPv4 address**.
2. Open a web browser and type:
   ```text
   http://<YOUR-EC2-PUBLIC-IP>/
   ```
   *(Example: `http://13.204.82.29/`)*

> [!WARNING]
> Always type **`http://`** and not `https://`. Web browsers often try to prepend `https://` automatically. Since this beginner project does not yet have an SSL certificate, typing `https://` will show a connection error.

---

## 📈 Cloud Monitoring & Observability Architecture

This project implements an enterprise-grade multi-tier monitoring strategy natively deployed across AWS services:

### 1. AWS CloudWatch Synthetics Canary (Headless Browser Uptime)
- **Canary Name:** `fcc-uptime-canary` (AWS Region: `ap-south-1`)
- **Mechanism:** Powered by AWS Lambda and Puppeteer, running headless browser checks every 5 minutes.
- **Verification:** Navigates to `http://13.204.82.29/`, validates `HTTP 200 OK`, captures visual screenshots to Amazon S3 (`s3://fcc-cw-canary-319634665438/`), and records end-to-end page load latency ($ms$).
- **Screenshot Evidence:** Verified in local repository at [`screenshots/aws_canary_verified_screenshot.png`](file:///c:/Users/JEETSINGH%20RAJPUT/Downloads/FCC/screenshots/aws_canary_verified_screenshot.png).

### 2. Amazon Route 53 Global Edge Health Checking
- **Health Check ID:** `b18efb43-f652-4a6a-9850-ccef8821e4dd`
- **Coverage:** Probed every 30 seconds across 8 global AWS regions (Tokyo, Singapore, Sydney, Ireland, Virginia, Oregon, California, São Paulo).
- **Status:** **100% HEALTHY** (`Success: HTTP Status Code 200, OK`).

### 3. Unified CloudWatch Executive Dashboard
- **Dashboard Name:** `FCC-Web-Hosting-Dashboard`
- **Location:** AWS Console &rarr; CloudWatch &rarr; Dashboards
- **Real-Time Widgets:**
  - 🚨 **Active Alarms:** Health state of `HighCPUUtilization-fcc-web-server` and `fcc-web-server-status-check-failed`.
  - ⚡ **CPU Utilization (%):** Time-series graph with 80% threshold line.
  - 🩺 **Reachability Checks:** System and Instance status check graphs (2/2 passed).
  - 🌐 **Network Throughput:** Inbound and outbound network bandwidth in bytes.
  - 🔍 **Canary Availability (%):** Live 24/7 uptime percentage calculated by AWS.
  - ⏱️ **Page Load Latency (ms):** End-to-end user experience timing.

### 4. Automated Alerting via Amazon SNS (Simple Notification Service)
- Configured **Amazon SNS Topic:** `arn:aws:sns:ap-south-1:319634665438:fcc-monitoring-alerts`
- Subscribed to both `StatusCheckFailed` (hypervisor crash) and `CPUUtilization` (>80%) alarms.
- Dispatches instant email alerts to the registered administrator address whenever thresholds are crossed.

### 5. Client-Side Real User Monitoring (RUM) & CLI Tools
- **Client RUM:** Uses W3C **Navigation Timing API** inside vanilla JavaScript (`app.js`) to log TTFB and DOM ready times.
- **Local CLI Tools:** [`scripts/uptime_monitor.py`](file:///c:/Users/JEETSINGH%20RAJPUT/Downloads/FCC/scripts/uptime_monitor.py) and [`scripts/UptimeMonitor.ps1`](file:///c:/Users/JEETSINGH%20RAJPUT/Downloads/FCC/scripts/UptimeMonitor.ps1) provide local synthetic testing and audit logging (`uptime_log.csv`).
- Full implementation details available in [docs/monitoring-guide.md](file:///c:/Users/JEETSINGH%20RAJPUT/Downloads/FCC/docs/monitoring-guide.md).

---

## 🛡️ Security using AWS IAM

Security in cloud computing relies on the **Principle of Least Privilege**: giving users and applications only the permissions they strictly need.

1. **Root Account Protection:**
   - The AWS root account is used only for account creation and billing setup, never for day-to-day work.
2. **Dedicated IAM User:**
   - A dedicated IAM user with limited permissions is created for project deployment.
3. **No Hardcoded Credentials:**
   - AWS access keys, secret keys, and `.pem` private keys are never committed to Git or pushed to GitHub.
4. **Least-Privilege S3 Policy:**
   - Any deployment policy (such as GitHub Actions deployment) is restricted only to the specific project S3 bucket rather than full administrative S3 permissions.

---

## 📋 Expected Output

When the deployment is complete, the following outputs confirm success:
- **Terminal Verification:**
  - Running `sudo systemctl status apache2` displays `Active: active (running)`.
  - Running `curl -I http://localhost` returns `HTTP/1.1 200 OK`.
- **Browser Output:**
  - Navigating to `http://<EC2-PUBLIC-IP>` displays the **Cloud-Based Website Hosting & Monitoring System Using AWS** homepage.
  - The page displays all project objectives, cloud architecture details, and interactive monitoring tools.
- **AWS Console Output:**
  - In the EC2 Dashboard, instance state displays green: **Running**.
  - Status check column displays: **2/2 checks passed**.
  - CloudWatch graph displays active CPU utilization data points.

---

## 🔮 Future Scope

This project establishes the foundation of cloud computing. Future enhancements could include:
1. **SSL/TLS Encryption (HTTPS):** Installing a free SSL certificate using Let's Encrypt / Certbot for secure encrypted web traffic on port 443.
2. **Domain Name Integration:** Mapping a custom domain name (e.g., `mycollegeproject.com`) to the EC2 Public IP using **Amazon Route 53**.
3. **Content Delivery Network (CDN):** Adding **Amazon CloudFront** to cache static assets in edge locations worldwide for faster loading speeds.
4. **Auto Scaling & Load Balancing:** Using an **Application Load Balancer (ALB)** and **Auto Scaling Group** to automatically launch more EC2 instances when visitor traffic increases.
5. **Database Integration:** Connecting a managed database like **Amazon RDS (MySQL / PostgreSQL)** to turn the static website into a full-stack dynamic web application.

---

## 🏁 Conclusion

Through this project, we successfully demonstrated the core concepts taught in **Fundamentals of Cloud Computing**:
- Understanding Infrastructure-as-a-Service (**IaaS**) by launching and managing a virtual Linux server in AWS EC2.
- Configuring a web server (**Apache**) to deliver web content over the internet.
- Applying network security boundaries using **AWS Security Groups**.
- Managing cloud storage with **Amazon S3** and access control with **AWS IAM**.
- Tracking virtual infrastructure health and resource utilization with **Amazon CloudWatch**.

This project provides practical, hands-on experience in cloud infrastructure fundamentals, server administration, and modern cloud operations suitable for a second-year B.Tech engineering curriculum.
