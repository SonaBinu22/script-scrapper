# SCRIPT SCRAPPER — WINDOWS RUNTIME VERIFICATION REPORT

**Verification Date:** November 6, 2026  
**Auditor:** DevOps Architect & Senior Backend Engineer  
**Host Target:** Windows 10/11 / Windows Server (64-bit)  
**Governance Milestone:** Gate 0 Closure Preparation  

---

## 1. EMPIRICAL RUNTIME VERIFICATION MATRIX

The underlying host machine was physically inspected via PowerShell commands on 2026-11-06. The actual verified status of each runtime component is recorded below:

| Runtime Component | Target Version | Verified State on Host | Status | Action Required |
| :--- | :--- | :--- | :---: | :--- |
| **Operating System** | Windows 10/11 64-bit | Windows 64-bit Architecture | **VERIFIED** | None. Standard Windows host confirmed. |
| **Python Runtime** | Python 3.11+ (64-bit) | **Python 3.13.5 (on PATH)** | **VERIFIED** | Ready for isolated virtual environment (`.venv`) creation in Gate 1. |
| **Version Control** | Git 2.40+ | **git version 2.47.1.windows.2** | **VERIFIED** | Ready for repository governance initialization. |
| **PowerShell Engine** | PowerShell 5.1+ / 7.x | **Windows PowerShell 5.1 / 7** | **VERIFIED** | Native automation scripts supported. |
| **PostgreSQL Engine** | PostgreSQL 16 (64-bit) | Not yet installed on system PATH | **PENDING** | Execute EnterpriseDB MSI installer during Gate 1 Foundation Setup. |
| **Reverse Proxy** | Caddy v2.7+ (64-bit) | Not yet installed on system PATH | **PENDING** | Download single static binary `caddy.exe` to PATH during Gate 1. |
| **OCR Engine** | Tesseract OCR v5.3+ | Not yet installed on system PATH | **PENDING** | Execute UB-Mannheim 64-bit installer during Gate 1. |

---

## 2. VERIFIED PYTHON ENVIRONMENT DETAILS

PowerShell verification command:
```powershell
python --version
# Output: Python 3.13.5
```

- **Architecture:** AMD64 / 64-bit.
- **Pip Availability:** Standard library `ensurepip` available.
- **Virtual Environment Tool:** Python standard `venv` module supported.

---

## 3. EXTERNAL RUNTIME INSTALLATION SPECIFICATION (FOR GATE 1)

In strict adherence to Gate 0 restrictions (*"Do not install dependencies, do not deploy infrastructure"*), installation of external runtime binaries is queued for Gate 1 (Foundation Setup):

### 3.1 PostgreSQL 16 Setup Specification
- **Installer:** Official EnterpriseDB PostgreSQL 16 for Windows 64-bit.
- **Service Name:** `postgresql-x64-16`
- **Default Port:** `5432`
- **Encoding:** `UTF8`
- **Collation:** `English_United States.1252` or `C.UTF-8`

### 3.2 Caddy v2 Setup Specification
- **Binary:** Official static Windows executable `caddy.exe` (v2.8+).
- **Placement:** Placed in system PATH (e.g. `C:\Tools\Caddy\caddy.exe` or repository root `tools/caddy.exe`).
- **Service Management:** Managed as a Windows Service via WinSW or NSSM:
  ```powershell
  nssm install ScriptScrapper-Proxy "C:\Tools\Caddy\caddy.exe" "run --config D:\script-scrapper\Caddyfile"
  ```

### 3.3 Tesseract OCR v5.3+ Setup Specification
- **Installer:** UB-Mannheim Tesseract OCR 64-bit installer.
- **Default Installation Directory:** `C:\Program Files\Tesseract-OCR\`
- **Language Pack:** English traineddata (`eng.traineddata`).
- **Path Verification:** `C:\Program Files\Tesseract-OCR\tesseract.exe --version`

---

## 4. WINDOWS HOST OPERATING SYSTEM OPTIMIZATIONS

During the Gate 1 foundation setup, the following Windows system registry setting must be validated:

```powershell
# Enable NTFS Long Paths (>260 characters)
Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" -Name "LongPathsEnabled" -Value 1
```

**Verification Verdict:** The core foundational runtimes (Python 3.13.5 64-bit and Git 2.47.1) are **VERIFIED and ready**. External system services are fully documented and ready for deployment in Gate 1 upon authorization.
