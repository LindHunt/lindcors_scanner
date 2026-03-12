# 🔥 lindcors_scanner - CORS Misconfiguration Scanner

<p align="center">
  <img src="https://img.shields.io/badge/Version-1.0-blue?style=for-the-badge" alt="Version">
  <img src="https://img.shields.io/badge/Python-3.6%2B-green?style=for-the-badge" alt="Python">
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="License">
  <img src="https://img.shields.io/badge/PRs-Welcome-brightgreen?style=for-the-badge" alt="PRs">
</p>

<pre align="center">
╔═══════════════════════════════════════════════════════════════╗
║  ██╗     ██╗███╗   ██╗██████╗ ███████╗ ██████╗ ██████╗ ███████╗ ║
║  ██║     ██║████╗  ██║██╔══██╗██╔════╝██╔═══██╗██╔══██╗██╔════╝ ║
║  ██║     ██║██╔██╗ ██║██║  ██║███████╗██║   ██║██████╔╝███████╗ ║
║  ██║     ██║██║╚██╗██║██║  ██║╚════██║██║   ██║██╔══██╗╚════██║ ║
║  ███████╗██║██║ ╚████║██████╔╝███████║╚██████╔╝██║  ██║███████║ ║
║  ╚══════╝╚═╝╚═╝  ╚═══╝╚═════╝ ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝ ║
║                    CORS SCANNER by LindHunt                      ║
╚═══════════════════════════════════════════════════════════════╝
</pre>

## 📋 About

**lindcors_scanner** is a lightweight CORS misconfiguration scanner for educational purposes only. It helps identify dangerous CORS settings that could lead to security vulnerabilities.

> just for education only

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| Single Target | Scan individual websites |
| Multi Target | Batch scan from file |
| Multi-threading | Fast scanning with threads |
| Severity Rating | CRITICAL, HIGH, MEDIUM |
| JSON Reports | Save results in JSON format |
| Text Reports | Save results in readable format |

---

## 🚀 Installation

```bash
git clone https://github.com/LindHunt/lindcors_scanner.git
cd lindcors_scanner
pip install requests
```

---

## 🎯 Usage

### Single Target
```bash
python lindcors.py -u https://example.com
```

### Multiple Targets
```bash
python lindcors.py -l targets.txt
```

### With Threads
```bash
python lindcors.py -l targets.txt -t 20
```

### Save Report
```bash
python lindcors.py -l targets.txt -o report
```

---

## 📊 Output Example

```
╔══════════════════════════════════════════════════════════════╗
║ VULNERABLE: https://example.com                              ║
╠══════════════════════════════════════════════════════════════╣
║ [CRITICAL] Origin: https://evil.com                         ║
║    ACAO: https://evil.com                                    ║
║    Credentials: true                                         ║
╚══════════════════════════════════════════════════════════════╝
```

---

## 🔍 Tested Origins

```
https://evil.com
https://evilsite.com
https://evil.com.attacker.com
https://attacker.com.evil.com
http://evil.com
null
```

---

## ⚠️ Disclaimer

This tool is for educational purposes only. Users are responsible for complying with applicable laws and obtaining proper authorization before scanning any targets.

---

## 📄 License

MIT License

Copyright (c) 2026 LindHunt

---

<p align="center">
  <sub>Built by LindHunt</sub>
</p>

<p align="center">
  <a href="#">Documentation</a> • <a href="#">Report Bug</a> • <a href="#">Request Feature</a>
</p>
