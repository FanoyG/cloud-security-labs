<div align="center">

# 🥈 IAM User with Long-Lived Access Keys → Credential Leakage

**Realistic SOC & Cloud Security Misconfiguration Lab**  
*Terraform + Python (Boto3)*

</div>

---

## 📋 Table of Contents

- [TL;DR](#tldr)
- [Overview](#overview)
- [Why This Scenario Matters](#-why-this-scenario-matters)
- [The Misconfiguration](#-the-misconfiguration)
- [Why This Is Dangerous](#️-why-this-is-dangerous-even-with-minimal-permissions)
- [Lab Architecture](#-lab-architecture)
- [Attack Results](#-attack-results)
- [Screenshots](#️-screenshots)
- [Correct Mitigation](#️-correct-mitigation)
- [Key Concepts](#-key-security-concepts-demonstrated)
- [Getting Started](#-getting-started)
- [Contributing](#-contributing)
- [License](#-license)

---

## TL;DR

Leaked IAM access keys create persistent AWS API access that bypasses MFA. Even minimal permissions represent a serious security risk. The correct fix is to eliminate static credentials and use IAM roles with STS-issued temporary credentials.

---

## Overview

This lab demonstrates a real-world AWS IAM misconfiguration where long-lived IAM access keys create a **persistent, silent attack surface** once credentials are leaked — even when permissions appear minimal and safe.

This is one of the most common AWS breach entry points and a frequent topic in SOC, cloud security, and incident response interviews.

Unlike privilege-escalation labs, this scenario focuses on **credential persistence, detection gaps, and cloud-native identity design**, which are often misunderstood by beginners.

### Intended Audience

This lab is designed for:

- SOC analysts and cloud security learners
- Cloud security / SOC interview preparation
- Understanding credential-based attack paths
- Practicing cloud-native security thinking
- Security engineers transitioning from on-prem to cloud

---

## 🎯 Why This Scenario Matters

Security teams and interviewers care about this scenario because it:

- **Maps to Real Breaches** — Directly reflects AWS compromises seen in production
- **Tests IAM Fundamentals** — Understanding IAM users vs IAM roles is critical
- **Highlights Design Flaws** — Demonstrates cloud-native identity and access design principles
- **Shows Risk Without Escalation** — Proves danger exists even with minimal permissions
- **SOC-Relevant** — Highly applicable to monitoring and detection workflows

This is **not theoretical** — credential leakage happens daily through development workflows.

---

## ❌ The Misconfiguration

An IAM user is configured with:

- ⚠️ Long-lived access keys
- ⚠️ No key rotation policy
- ⚠️ Permissions that appear minimal and harmless
- ⚠️ API access that bypasses MFA

### Common Real-World Leak Sources

Credentials are frequently exposed through:

- Public GitHub repositories
- CI/CD pipeline logs
- Local `.env` files in version control
- Developer laptops infected with malware
- Misconfigured backups or application logs
- Third-party SaaS integrations

---

## ⚠️ Why This Is Dangerous (Even with Minimal Permissions)

Even when permissions are tightly scoped:

| Risk Factor | Impact |
|------------|--------|
| **MFA Bypass** | Access keys work without MFA |
| **Location Independence** | API access works from anywhere globally |
| **Silent Operation** | Compromise leaves minimal trace |
| **Persistence** | Credentials remain valid until manually revoked |
| **Detection Gaps** | Requires logging and monitoring, not just IAM config |

**The core problem is persistent authenticated access, not what the attacker can do today.**

An attacker with valid credentials can:
- Maintain long-term access for reconnaissance
- Wait for permission changes or misconfigurations
- Use credentials as a foothold for lateral movement
- Exfiltrate data within authorized scope

---

## 🧱 Lab Architecture

### Terraform – Misconfiguration Setup

Terraform is used to intentionally deploy the insecure state in a reproducible and auditable way.

**What This Lab Creates:**

1. Creates an IAM user
2. Attaches a minimal permission policy (`s3:ListAllMyBuckets`)
3. Generates a long-lived access key
4. Avoids MFA to demonstrate API access bypass

**Why Terraform?**

- ✅ Reproducible across environments
- ✅ Auditable infrastructure changes
- ✅ Infrastructure-as-Code best practices
- ✅ Easy cleanup with `terraform destroy`

> **Note:** Terraform does **not** perform the attack — it only creates the vulnerable condition.

---

### Python – Attack Demonstration (Boto3)

A Python script simulates an attacker who has obtained leaked credentials.

**The Script:**

1. Loads credentials from a local `.env` file
2. Authenticates using `boto3`
3. Performs a valid AWS API call (`ListBuckets`)
4. Demonstrates successful access without MFA or console login

**What This Proves:**

- ✓ Credentials are valid and functional
- ✓ API access works silently from any location
- ✓ Console access is not required
- ✓ Minimal permissions still create exploitable risk

---

## 🧪 Attack Results

### Expected Output

```
[+] API call successful
Buckets visible to attacker:
[-] No buckets available in this account
```

### Interpreting the Results

This result is **expected and demonstrates the vulnerability**:

- ✅ **Successful API execution** confirms authentication works
- ✅ **Empty results** only reflect authorization scope
- ⚠️ **The security risk still exists** due to persistent access

The attacker has proven they can authenticate. The lack of accessible resources is irrelevant to the core vulnerability.

---

## 🖼️ Screenshots

This repository includes high-signal screenshots to validate execution:

### 1. Terraform Apply (Misconfiguration Creation)

<p align="center">
    <img src="./llak-images/image_1.png" alt="Terraform Apply Step 1" width="600">
</p>

<p align="center">
    <img src="./llak-images/image_2.png" alt="Terraform Apply Step 2" width="600">
</p>

### 2. Python Attack Output (API Access Proof)

<p align="center">
    <img src="./llak-images/image_3.png" alt="Python Attack Output" width="600">
</p>

### 3. AWS Console View (IAM User and Policy)

<p align="center">
    <img src="./llak-images/image_4.png" alt="AWS Console IAM User" width="600">
</p>

<p align="center">
    <img src="./llak-images/image_5.png" alt="AWS Console Policy" width="600">
</p>

### 4. Terraform Destroy (Responsible Cleanup)

<p align="center">
    <img src="./llak-images/image_6.png" alt="Terraform Destroy Step 1" width="600">
</p>

<p align="center">
    <img src="./llak-images/image_7.png" alt="Terraform Destroy Step 2" width="600">
</p>

**🔒 Security Note:**  
All sensitive identifiers (account IDs, ARNs, access key IDs, timestamps) are redacted. All credentials were destroyed immediately after demonstration. Screenshots exist only to prove execution, not to expose secrets.

---

## 🛡️ Correct Mitigation

### ❌ Wrong Approach

- Rotating keys more frequently
- Adding more restrictive policies
- Implementing IP allowlists
- Setting expiration notifications

**These approaches treat the symptom, not the disease.**

### ✅ Recommended Cloud-Native Fix

1. **Delete IAM Access Keys**
   - Remove all long-lived credentials immediately

2. **Eliminate IAM Users for Workloads**
   - Use IAM roles for EC2, Lambda, ECS, and other services
   - Use identity federation for human access

3. **Use STS-Issued Temporary Credentials**
   - Credentials automatically expire
   - Reduced blast radius if compromised

4. **Enforce MFA During Role Assumption**
   - Where applicable for human access
   - Adds defense-in-depth

5. **Enable Logging and Monitoring**
   - CloudTrail for API activity
   - CloudWatch for anomaly detection
   - AWS Config for compliance monitoring

### The Golden Rule

**You don't secure bad credentials — you eliminate them.**

---

## 🧠 Key Security Concepts Demonstrated

| Concept | What You'll Learn |
|---------|-------------------|
| **Credential Leakage** | How credentials escape secure environments |
| **Long-Lived Credentials** | Why static keys are a persistent risk |
| **MFA Limitations** | When MFA doesn't protect you |
| **Silent Persistence** | How compromises remain undetected |
| **Detection vs Prevention** | Why monitoring alone isn't enough |
| **IAM Roles Over Users** | Cloud-native identity patterns |
| **Cloud-Native Design** | How to think about identity in AWS |

---

## 🚀 Getting Started

### Prerequisites

- AWS account (isolated lab environment recommended)
- Terraform installed (`>= 1.0`)
- Python 3.x with Boto3
- AWS CLI configured

### Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. **Deploy the Infrastructure**
   ```bash
   cd terraform/
   terraform init
   terraform apply
   ```

3. **Configure Python Environment**
   - Create a `.env` file with the generated credentials
   - Install dependencies: `pip install -r requirements.txt`

4. **Execute the Attack Simulation**
   ```bash
   python whoami.py
   python enumerate.py
   python attack.py
   ```

5. **Clean Up Resources**
   ```bash
   cd terraform/
   terraform destroy
   ```

### ⚠️ Important Notes

- Always use an **isolated AWS account** for security labs
- Never test in production environments
- Ensure all resources are destroyed after testing
- Review AWS costs before deployment (this lab is minimal-cost)

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

This is a learning-focused security lab, and community feedback improves clarity and accuracy.

**How to Contribute:**
- Open an issue for bugs or suggestions
- Submit pull requests for improvements
- Share feedback on clarity and educational value

---

## ⚠️ Disclaimer

This project simulates insecure AWS IAM configurations **for educational purposes only**.

- ✅ All testing must be performed in isolated lab accounts
- ✅ Never deploy these configurations in production
- ✅ The author assumes no responsibility for misuse
- ✅ Use responsibly and ethically

---

## 📄 License

This project is for educational purposes only. Use responsibly and ethically.

---

## 📞 Questions or Feedback?

If you have questions about this lab or suggestions for improvement, please open an issue or reach out through the repository's discussion board.

**Happy Learning! 🎓🔒**