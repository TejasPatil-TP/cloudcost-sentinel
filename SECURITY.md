# Security Policy

## Supported Versions

We actively maintain and provide security updates for the following versions of CloudCost Sentinel:

| Version | Supported          |
| :------ | :----------------- |
| `1.0.x` | :white_check_mark: |
| `< 1.0` | :x:                |

---

## Reporting a Vulnerability

Security is paramount when handling cloud financial records and infrastructure telemetry. If you discover a security vulnerability in CloudCost Sentinel, please report it responsibly:

* **Email:** Send your disclosure to [tejaspatil2626@gmail.com](mailto:tejaspatil2626@gmail.com).
* **Please DO NOT file public GitHub issues for security vulnerabilities.**

### Information to Include in Your Report
To help us triage and resolve the issue quickly, please provide:
1. A detailed description of the vulnerability and its potential impact.
2. Steps to reproduce the issue, including proof-of-concept scripts or synthetic payloads.
3. Any suggested remediations or workarounds.

### Response & Disclosure Process
* **Acknowledgment:** We will acknowledge receipt of your report within 48 hours.
* **Assessment:** We will assess the severity and work on a fix in a private branch.
* **Resolution:** A security advisory and patch will be released. We will publicly credit your contribution unless you prefer to remain anonymous.

---

## Security Considerations & Best Practices

CloudCost Sentinel is currently an open-source FinOps platform in MVP status:

1. **Local and Private Deployments:** Authentication (OIDC / OAuth2) and Role-Based Access Control (RBAC) are not yet implemented. **Do not expose the application or its API directly to the public internet** without an authenticating reverse proxy or API gateway.
2. **Billing File Confidentiality:** Cloud provider billing exports (AWS CUR, Azure Cost Management, GCP BigQuery) often contain sensitive financial amounts and internal account identifiers. Ensure files are transmitted over secure channels and stored with restricted permissions.
3. **Payload Size Restrictions:** The backend enforces a strict **10MB upload limit** on all CSV endpoints to protect against resource exhaustion and denial-of-service attempts.
4. **Environment Secrets:** Never commit `.env` files, database passwords, or Redis connection strings to version control. Use `.gitignore` to maintain secret hygiene.
