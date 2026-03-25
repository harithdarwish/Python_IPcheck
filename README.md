# IP Threat Intelligence & Security Analysis

## 📌 Project Overview
This Python tool automates the process of identifying and validating malicious IP addresses. It pulls data from **GitHub** security lists and cross-references them with **AbuseIPDB**, **IPinfo**, and **CleanTalk** APIs to confirm threats.

## 🛠️ How it Works
1. **Fetch:** Pulls raw IP lists from public GitHub repositories.
2. **Scan:** Checks each IP against **AbuseIPDB**, **IPinfo**, and **CleanTalk** for recent reports.
3. **Export:** Generates a clean **Excel (.xlsx)**. 
4. **Validate:** Uses **VirusTotal** to see how many security vendors (Kaspersky, Sophos, etc.) flag the IP.

### Prerequisites
- Python 3.x
- API Keys for AbuseIPDB, IPinfo, VirusTotal and any Network OSINT.
