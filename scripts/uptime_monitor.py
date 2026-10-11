#!/usr/bin/env python3
"""
==============================================================================
Website Uptime and Response Time Monitor
Course: Fundamentals of Cloud Computing (Second-Year B.Tech)
Project: Cloud-Based Website Hosting and Monitoring System Using AWS
==============================================================================
This script performs synthetic uptime monitoring for our live AWS EC2 website:
1. Sends HTTP GET requests to the website URL/IP.
2. Verifies whether the server returns HTTP Status 200 OK.
3. Tracks round-trip response latency in milliseconds.
4. Detects outages, connection failures, and timeouts.
5. Logs results to a CSV file for faculty evaluation and audit reporting.
==============================================================================
"""

import sys
import time
import argparse
import csv
from datetime import datetime
import urllib.request
import urllib.error

# ANSI Color codes for clean terminal presentation
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"

DEFAULT_TARGET_URL = "http://13.204.82.29/"
DEFAULT_TIMEOUT_SEC = 5
DEFAULT_INTERVAL_SEC = 5
DEFAULT_LOG_FILE = "uptime_log.csv"

def check_website(url: str, timeout: int = DEFAULT_TIMEOUT_SEC):
    """
    Checks the website health and measures response latency in milliseconds.
    Returns: (status_code, response_time_ms, is_up, error_message)
    """
    start_time = time.perf_counter()
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "AWS-Cloud-Uptime-Monitor/2.0 (B.Tech Course Project)"}
    )
    
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            latency_ms = (time.perf_counter() - start_time) * 1000.0
            status_code = response.getcode()
            is_up = (200 <= status_code < 400)
            return status_code, round(latency_ms, 2), is_up, "OK"
    except urllib.error.HTTPError as e:
        latency_ms = (time.perf_counter() - start_time) * 1000.0
        return e.code, round(latency_ms, 2), False, f"HTTP Error {e.code}"
    except urllib.error.URLError as e:
        latency_ms = (time.perf_counter() - start_time) * 1000.0
        return 0, round(latency_ms, 2), False, f"Connection Failed: {e.reason}"
    except Exception as e:
        latency_ms = (time.perf_counter() - start_time) * 1000.0
        return 0, round(latency_ms, 2), False, f"Exception: {str(e)}"

def initialize_csv(log_path: str):
    """Ensures CSV log header exists."""
    try:
        with open(log_path, mode="a", newline="", encoding="utf-8") as f:
            if f.tell() == 0:
                writer = csv.writer(f)
                writer.writerow(["Timestamp", "Target_URL", "HTTP_Status", "Latency_ms", "Result", "Notes"])
    except IOError as e:
        print(f"{YELLOW}[WARN] Could not initialize CSV file {log_path}: {e}{RESET}")

def append_csv_log(log_path: str, timestamp: str, url: str, status: int, latency: float, result: str, notes: str):
    """Appends a single health check entry to the audit log."""
    try:
        with open(log_path, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, url, status, latency, result, notes])
    except IOError:
        pass

def main():
    parser = argparse.ArgumentParser(description="Live Website Uptime & Response Time Monitor for AWS EC2")
    parser.add_argument("--url", default=DEFAULT_TARGET_URL, help=f"Target URL to monitor (default: {DEFAULT_TARGET_URL})")
    parser.add_argument("--interval", type=int, default=DEFAULT_INTERVAL_SEC, help="Interval between checks in seconds (default: 5)")
    parser.add_argument("--count", type=int, default=0, help="Total number of checks to run (0 for infinite until Ctrl+C)")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT_SEC, help="Connection timeout in seconds (default: 5)")
    parser.add_argument("--csv", default=DEFAULT_LOG_FILE, help=f"CSV file to record results (default: {DEFAULT_LOG_FILE})")
    args = parser.parse_args()

    # Clean URL format
    target_url = args.url.strip()
    if not (target_url.startswith("http://") or target_url.startswith("https://")):
        target_url = "http://" + target_url

    initialize_csv(args.csv)

    print(f"\n{CYAN}{BOLD}{'='*72}{RESET}")
    print(f"{CYAN}{BOLD}  AWS EC2 LIVE WEBSITE UPTIME & LATENCY MONITOR                      {RESET}")
    print(f"{CYAN}  Course: Fundamentals of Cloud Computing (Second-Year B.Tech)       {RESET}")
    print(f"{CYAN}{BOLD}{'='*72}{RESET}")
    print(f"  Target Website  : {BOLD}{target_url}{RESET}")
    print(f"  Timeout Window  : {args.timeout} seconds")
    print(f"  Check Frequency : Every {args.interval} seconds")
    print(f"  Audit CSV Log   : {args.csv}")
    print(f"{CYAN}{'-'*72}{RESET}")
    print(f" {'Timestamp':<20} | {'Status':<10} | {'Latency':<12} | {'Result':<10} | {'Details'}")
    print(f"{CYAN}{'-'*72}{RESET}")

    total_checks = 0
    successful_checks = 0
    failed_checks = 0
    latencies = []

    try:
        while True:
            total_checks += 1
            now_iso = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            status, latency, is_up, details = check_website(target_url, timeout=args.timeout)
            
            if is_up:
                successful_checks += 1
                latencies.append(latency)
                status_str = f"{GREEN}{status} OK{RESET}"
                result_badge = f"{GREEN}[UP]{RESET}"
                append_csv_log(args.csv, now_iso, target_url, status, latency, "UP", details)
            else:
                failed_checks += 1
                status_str = f"{RED}{status if status > 0 else 'TIMEOUT'}{RESET}"
                result_badge = f"{RED}[DOWN]{RESET}"
                append_csv_log(args.csv, now_iso, target_url, status, latency, "DOWN", details)

            print(f" {now_iso:<20} | {status_str:<19} | {latency:>7.2f} ms   | {result_badge:<19} | {details}")

            if args.count > 0 and total_checks >= args.count:
                break

            time.sleep(args.interval)

    except KeyboardInterrupt:
        print(f"\n{YELLOW}[INFO] Monitoring session stopped by user.{RESET}")

    # Summary Statistics
    uptime_pct = (successful_checks / total_checks * 100.0) if total_checks > 0 else 0.0
    avg_latency = (sum(latencies) / len(latencies)) if latencies else 0.0
    min_latency = min(latencies) if latencies else 0.0
    max_latency = max(latencies) if latencies else 0.0

    print(f"\n{CYAN}{BOLD}{'='*72}{RESET}")
    print(f"{CYAN}{BOLD}  MONITORING AUDIT SUMMARY                                            {RESET}")
    print(f"{CYAN}{BOLD}{'='*72}{RESET}")
    print(f"  Total Checks Executed  : {total_checks}")
    print(f"  Successful (HTTP 200)  : {GREEN}{successful_checks}{RESET}")
    print(f"  Failures (Downtime)    : {RED if failed_checks > 0 else GREEN}{failed_checks}{RESET}")
    print(f"  Calculated Uptime      : {GREEN if uptime_pct >= 99 else YELLOW}{uptime_pct:.2f}%{RESET}")
    if latencies:
        print(f"  Average Response Time  : {avg_latency:.2f} ms")
        print(f"  Fastest Response (Min) : {min_latency:.2f} ms")
        print(f"  Slowest Response (Max) : {max_latency:.2f} ms")
    print(f"  Audit Log Saved To     : {args.csv}")
    print(f"{CYAN}{'='*72}{RESET}\n")

if __name__ == "__main__":
    main()
