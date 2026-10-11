# 📊 Final Project Presentation Slides (PPT Content)

**Course:** Fundamentals of Cloud Computing  
**Level:** Second-Year B.Tech Course Project  
**Project Title:** Cloud-Based Website Hosting and Monitoring System Using AWS  
**Student Name:** Jeet Singh Rajput  
**Target Environment:** AWS EC2 (Ubuntu 22.04 LTS, Apache2) | Mumbai (`ap-south-1`)  
**Live Target Website:** `http://13.204.82.29/`

---

## Slide 1: Title Slide

- **Slide Title:** Cloud-Based Website Hosting and Monitoring System Using AWS
- **Subtitle:** An Enterprise Multi-Tier Web Hosting and Cloud Observability Architecture
- **Course:** Fundamentals of Cloud Computing (Second-Year B.Tech)
- **Presented By:** Jeet Singh Rajput
- **Target Cloud Environment:** Amazon Web Services (AWS) | Mumbai Region (`ap-south-1`)
- **Live Public URL:** `http://13.204.82.29/`

> **🎙️ Speaker Notes:**  
> *"Good morning respected faculty and course guide. Today, I am presenting my Fundamentals of Cloud Computing course project: 'Cloud-Based Website Hosting and Monitoring System Using AWS'. This project showcases Infrastructure-as-a-Service provisioning, web server administration, and an enterprise-grade cloud observability and automated incident response pipeline."*

---

## Slide 2: Introduction & Cloud Paradigm

- **Traditional On-Premise / Local Hosting Limitations:**
  - High risk of single points of failure (power loss, hardware crashes).
  - Websites stop working when a personal laptop is closed or disconnected from Wi-Fi.
  - Requires physical hardware procurement, manual networking, and expensive maintenance.
- **The Cloud Computing Solution:**
  - On-demand computing power, scalable network bandwidth, and persistent storage.
  - High availability ($99.99\%$) backed by AWS Global Infrastructure.
  - Pay-as-you-go cost model with zero initial physical hardware capital expense.

> **🎙️ Speaker Notes:**  
> *"In traditional computing, running a web server on a local machine is fragile. If the machine sleeps or loses power, the service dies. Cloud computing transforms this by letting us rent virtual servers, resilient network firewalls, and automated monitoring systems over the internet on AWS."*

---

## Slide 3: Problem Statement

- **1. Availability Deficit:** Personal development servers (`localhost:8000`) cannot guarantee 24/7 uptime.
- **2. Public Accessibility Barriers:** Local development cannot be reached by external internet users without risky router port forwarding.
- **3. Zero Operational Visibility:** When a local web server crashes or runs out of RAM, administrators have no mechanism to detect the failure or receive alerts.
- **4. Network Security Exposure:** Directly exposing personal machines to the internet creates severe vulnerabilities without perimeter firewalls and access controls.

> **🎙️ Speaker Notes:**  
> *"The problem we address is twofold: First, delivering high availability and global reachability for web applications. Second, eliminating the visibility gap where web servers crash silently without notifying administrators."*

---

## Slide 4: Project Objectives

- **1. IaaS Cloud Provisioning:** Deploy a secure, high-performance Ubuntu Linux virtual instance on **Amazon EC2 (`t3.micro`)**.
- **2. Web Server Management:** Install and configure the production **Apache HTTP Server (`apache2`)** listening on Port 80.
- **3. Network & Identity Security:** Enforce perimeter security using **AWS Security Groups** and apply least-privilege access using **AWS IAM**.
- **4. Multi-Tier Observability:** Implement a 3-tier monitoring pipeline combining:
  - Internal VM hypervisor metrics (**CloudWatch**).
  - External headless browser testing (**CloudWatch Synthetics Canary**).
  - Global edge reachability checks (**Amazon Route 53**).
- **5. Automated Incident Response:** Connect threshold alarms to **Amazon SNS** for instant email notification and recovery alerts.

> **🎙️ Speaker Notes:**  
> *"Our objective was not merely to deploy static HTML files, but to implement a complete production-grade cloud workflow: automated deployment, virtual firewalling, and end-to-end telemetry."*

---

## Slide 5: System Architecture & Data Flow

- **Visual Layout:** (Include the Architecture Diagram from README)
  - `Client / Global Probes` &rarr; `Internet` &rarr; `Security Group (Port 80/22)` &rarr; `EC2 Instance (Apache)`
  - Parallel Observability:
    - **Route 53 Global Health Probes:** Probing from 8 AWS regions worldwide.
    - **CloudWatch Synthetics:** Headless Chromium canary running every 5 minutes on Lambda.
    - **Amazon S3:** Durable storage for canary screenshot artifacts (`s3://fcc-cw-canary-319634665438/`).
    - **CloudWatch Dashboard & SNS:** Alerting pipeline delivering emails to administrator.

> **🎙️ Speaker Notes:**  
> *"This architecture demonstrates a dual-layer interaction: The primary path handles inbound user HTTP requests on Port 80 protected by our Security Group. Simultaneously, our observability tier probes the instance from 8 global AWS regions and dispatches incident emails via SNS if thresholds breach."*

---

## Slide 6: Technology Stack

| Category | Technology | Role & Purpose |
| :--- | :--- | :--- |
| **Cloud Provider** | Amazon Web Services (AWS) | Core infrastructure host in Mumbai (`ap-south-1`) |
| **Virtual Compute** | Amazon EC2 (`t3.micro`) | 2 vCPU, 1 GiB Memory virtual server running Ubuntu 22.04 LTS |
| **Web Server** | Apache HTTP Server (`apache2`) | Listens on port 80, serves web assets from `/var/www/html/` |
| **Storage & Artifacts** | Amazon S3 | High-durability storage for canary screenshots & logs |
| **Synthetic Monitoring**| AWS CloudWatch Synthetics | Headless browser (Puppeteer) automated testing |
| **Global DNS Health** | Amazon Route 53 | Multi-region external health probing (8 regions) |
| **Alerting Pipeline** | Amazon SNS | Push notification topic dispatching instant alarm & recovery emails |
| **Client Frontend** | HTML5, CSS3, Vanilla JS | Lightweight, dark-themed responsive UI with W3C RUM telemetry |

> **🎙️ Speaker Notes:**  
> *"We utilized a lean, cost-efficient technology stack that combines native AWS building blocks with open-source web standards, adhering strictly to second-year curriculum requirements."*

---

## Slide 7: ⭐ NEW CHANGES & GUIDE RECOMMENDATIONS IMPLEMENTATION
*(Key Presentation Slide — Dedicated to faculty feedback implementation)*

- **1. Uptime Checking / Synthetic Monitoring (Implemented in AWS):**
  - Provisioned **AWS CloudWatch Synthetics Canary (`fcc-uptime-canary`)**: Runs headless Chromium via Puppeteer every 5 min, validates HTTP 200 OK, and stores screenshots in S3.
  - Configured **Amazon Route 53 Global Health Checks**: Probing across **8 worldwide regions** (100% Healthy).
- **2. Real User Monitoring / RUM (Implemented Client-Side):**
  - Integrated W3C **Navigation Timing API** into `app.js` to measure real visitor **TTFB** (Time to First Byte) and **DOM Ready Latency** without paid Cognito subscriptions.
- **3. Root Cause Analysis & Alerting (Implemented in AWS):**
  - Provisioned **Amazon SNS Topic (`fcc-monitoring-alerts`)** connected to CloudWatch alarms.
  - Successfully verified **both ALARM and OK Recovery email delivery** to administrator inbox.
  - Root cause diagnosis enabled via `/var/log/apache2/error.log` and `journalctl`.
- **4. Unified CloudWatch Executive Dashboard (New Feature):**
  - Created **`FCC-Web-Hosting-Dashboard`** with 6 real-time widgets in the AWS Console.
- **5. Architectural Defense for DB & SSL:**
  - **No Database:** Architecturally defended — this is a static website; faking database monitoring would be technically incorrect.
  - **SSL/Domain:** Documented as **Phase 2 Future Scope** to remain within credit/free-tier boundaries.

> **🎙️ Speaker Notes:**  
> *"Based on our course guide's recommendations, we implemented a comprehensive upgrade. We added AWS Synthetics Canaries with headless browser screenshots, Route 53 global health checking, an SNS alerting pipeline with recovery emails, client-side RUM, and a central CloudWatch executive dashboard. Every suggestion was addressed with real engineering rigor."*

---

## Slide 8: Deep-Dive: 3-Tier Observability Architecture

- **Tier 1: Internal Infrastructure Metrics (Amazon CloudWatch)**
  - Hypervisor-level sampling: `CPUUtilization`, `StatusCheckFailed`, `NetworkIn`, `NetworkOut`.
  - Configured Alarms: High CPU threshold (>80%) and System Status Check failure ($>= 1$).
- **Tier 2: External Synthetic Monitoring (Synthetics & Route 53)**
  - Blackbox testing simulating real internet visitors from outside AWS VPC.
  - Route 53 probes 8 global nodes (Tokyo, Singapore, Sydney, Ireland, Virginia, Oregon, California, São Paulo).
  - Lambda Puppeteer canary captures visual DOM rendering proof in S3.
- **Tier 3: Real User Monitoring / RUM (W3C Navigation Timing)**
  - Client-side browser performance telemetry capturing actual end-user network transit and HTML render latency.

> **🎙️ Speaker Notes:**  
> *"Modern cloud systems cannot rely on a single monitoring tool. We established a 3-tier strategy: Tier 1 watches the server hardware; Tier 2 simulates external users through headless browsers and worldwide DNS probes; Tier 3 captures real visitor browser telemetry."*

---

## Slide 9: Automated Incident Response & Alerting Pipeline

- **Alert Lifecycle:**
  1. **Detection:** CloudWatch samples metrics every 60 seconds against defined evaluation periods.
  2. **Breach:** If `StatusCheckFailed >= 1` or `CPUUtilization > 80%`, alarm state shifts from `OK` &rarr; `ALARM`.
  3. **Notification:** CloudWatch publishes an event payload to Amazon SNS (`fcc-monitoring-alerts`).
  4. **Push Dispatch:** Amazon SNS immediately formats and dispatches an alert email to the administrator.
  5. **Auto-Recovery:** When metric values fall back below threshold, `OKActions` triggers an **OK Recovery Email**.
- **Root Cause Analysis (RCA) Protocol:**
  - Administrator SSHs into EC2: `ssh -i fcc-ec2-key.pem ubuntu@13.204.82.29`
  - Inspects web server error stream: `sudo tail -n 50 /var/log/apache2/error.log`
  - Inspects kernel/systemd logs: `sudo journalctl -u apache2 --since "10 minutes ago"`

> **🎙️ Speaker Notes:**  
> *"Here is our incident response pipeline. Crucially, our system does not just sound an alarm when things break — it also confirms when service is restored through automated recovery notifications, providing a closed-loop monitoring cycle."*

---

## Slide 10: Live Demonstration & Results

- **Live URL:** `http://13.204.82.29/`
- **Verification Milestones Achieved:**
  - ✅ **Web Server Health:** Apache service active, returns `HTTP 200 OK` in <80 ms.
  - ✅ **CloudWatch Dashboard:** Active in AWS Console (`FCC-Web-Hosting-Dashboard`).
  - ✅ **Route 53 Global Status:** 8/8 worldwide regions reporting `Healthy`.
  - ✅ **CloudWatch Canary:** 100% Success rate, visual screenshot verified in S3.
  - ✅ **SNS Email Delivery:** Live ALARM and OK emails successfully received in administrator inbox.
  - ✅ **Local CLI Audit:** `uptime_monitor.py` generated audit trail in `uptime_log.csv`.

> **🎙️ Speaker Notes:**  
> *"During our live test, we verified all systems operating synchronously. The website is live, the CloudWatch Dashboard displays real-time telemetry, and our SNS email alerting pipeline has been verified with live inbox delivery."*

---

## Slide 11: Cloud Economics & Resource Optimization

- **Resource Budgeting & Cost Control:**
  - **EC2 `t3.micro`:** Eligible under AWS Free Tier (750 hours/month free).
  - **CloudWatch Dashboards:** First 3 dashboards are 100% Free.
  - **Amazon SNS:** 1,000 email notifications/month included in AWS Free Tier.
  - **Route 53 Health Checks:** ~$0.50 / month.
  - **CloudWatch Synthetics Canary:** ~$1.20 / month.
- **Credit Health:**
  - Supported by **$100.00 USD AWS Credit** valid for 162 days.
  - Total operational run rate: **<$2.00 / month**, leaving **98%+ of credit untouched**.
  - No unexpected billing surprises; enforced via AWS Budgets.

> **🎙️ Speaker Notes:**  
> *"Good cloud engineering requires cost optimization. We utilized our AWS credits strategically: running high-value enterprise features like Route 53 health checks and Puppeteer canaries for less than $2.00 per month, keeping 98% of our credit balance safe."*

---

## Slide 12: Future Scope & Enhancement Roadmap

- **Phase 2 Roadmap:**
  - **1. Custom Domain & Route 53 DNS:** Registering a custom top-level domain (`fcc-webhosting.com`) and routing traffic via Route 53 Hosted Zones.
  - **2. SSL/TLS Certificate (HTTPS):** Implementing AWS Certificate Manager (ACM) or Let's Encrypt for encrypted Port 443 web traffic.
  - **3. Amazon CloudFront (CDN):** Global edge caching to reduce Time To First Byte (TTFB) to single-digit milliseconds worldwide.
  - **4. Elastic Load Balancing & Auto Scaling:** Deploying an Application Load Balancer (ALB) across multiple Availability Zones to handle large traffic surges.
  - **5. Database Tier (Amazon RDS):** Integrating MySQL / PostgreSQL to evolve the static site into a dynamic full-stack cloud application.

> **🎙️ Speaker Notes:**  
> *"While our current phase demonstrates core IaaS hosting and observability, our architecture is built to evolve. Phase 2 introduces HTTPS encryption, global CDN caching via CloudFront, and managed databases via Amazon RDS."*

---

## Slide 13: Conclusion & Key Learnings

- **Core Competencies Demonstrated:**
  - **Cloud Infrastructure (IaaS):** Launching, configuring, and securing virtual machines in AWS EC2.
  - **Server Administration:** Linux package management, systemd service lifecycle, and Apache virtual hosting.
  - **Cloud Security:** Implementing virtual firewall rules (Security Groups) and IAM least privilege.
  - **Enterprise Observability:** Multi-tier monitoring spanning CloudWatch, Synthetics, Route 53, and SNS.
  - **Automation & DevOps:** Infrastructure scripting via Bash (`deploy.sh`), Python, and PowerShell.
- **Curriculum Alignment:** Fully satisfies second-year B.Tech Fundamentals of Cloud Computing learning outcomes.

> **🎙️ Speaker Notes:**  
> *"In conclusion, this project gave us hands-on, practical engineering experience with the foundational pillars of cloud computing: compute, security, networking, and observability. Thank you for your guidance throughout this project."*

---

## Slide 14: Q&A & Faculty Viva Defense

- **Common Evaluator Questions & Quick Reference Answers:**
  - **Why not monitor an API or Database?**  
    *Ans:* Our application is architected as a static website served directly by Apache. Claiming database monitoring would be architecturally inaccurate.
  - **Why did you use Synthetics instead of just CPU metrics?**  
    *Ans:* CPU metrics only reflect server hardware. A web server process can crash while CPU remains at 5%. Synthetics tests the real user experience from the internet.
  - **How did you test the alerting system?**  
    *Ans:* We simulated alarm state transitions using AWS CLI, verifying that CloudWatch triggers Amazon SNS and delivers real email notifications for both alarm and recovery states.

> **🎙️ Speaker Notes:**  
> *"Thank you. I am now ready for any questions or viva discussion."*
