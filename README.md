# PortScannerPractice

A modular, educational Python-based port scanning tool designed for cybersecurity practice, host exploration, service identification, and knowledge testing.

---

## ⚠️ ETHICAL DISCLAIMER & LEGAL NOTICE

> **FOR EDUCATIONAL AND AUTHORIZED TESTING PURPOSES ONLY.**
> 
> Port scanning without explicit, written authorization from the target network owner is illegal and unethical in many jurisdictions. Unauthorized scanning may violate computer crime laws (such as the US Computer Fraud and Abuse Act) and network service terms.
> 
> **Always ensure you have permission before scanning any system.** Use legally authorized targets such as `localhost`, internal lab virtual machines (e.g., Metasploitable, TryHackMe, Hack The Box), or public authorized test targets like `scanme.nmap.org`.

---

## 🚀 Features

- **Multi-Threaded TCP Port Scanning:** Fast and configurable concurrent socket connection testing across single ports or port ranges.
- **Service Identification:** Automatically maps detected open ports against a database of standard well-known network services and explains their security implications.
- **Banner Grabbing:** Optional service banner retrieval to identify software versions running on open ports.
- **Interactive Console Menu:** Easy-to-use menu system for interactive execution without memorizing CLI arguments.
- **Interactive Cybersecurity Quiz:** Study helper with randomized and static multiple-choice questions to reinforce network protocol and port knowledge.
- **Multi-Format Exporting:** Save detailed scan reports in **JSON**, **CSV**, or formatted human-readable **TXT** files.

---

## 📋 Requirements & Installation

### Requirements
- Python 3.7 or higher
- Standard Python libraries (`socket`, `threading`, `concurrent.futures`, `json`, `csv`, `argparse`, `sys`, `signal`) — **No external dependencies required!**

### Installation
1. Clone or download the repository:
   ```bash
   git clone https://github.com/your-username/PortScannerPractice.git
   cd PortScannerPractice
   ```
2. Verify Python version:
   ```bash
   python3 --version
   ```

---

## 💻 Usage

### Command Line Interface

`PortScannerPractice` supports both command-line flag execution and an interactive menu.

#### CLI Arguments

| Short | Long | Type | Default | Description |
|---|---|---|---|---|
| `-t` | `--target` | String | *None* | Target IP address or domain name (e.g. `127.0.0.1` or `scanme.nmap.org`) |
| `-p` | `--ports` | String | `1-1024` | Port range (`20-100`) or single port (`80`) |
| | `--timeout` | Float | `2.0` | Socket connection timeout in seconds |
| | `--threads` | Int | `10` | Number of concurrent scanning threads |
| `-b` | `--banner` | Flag | `False` | Enable HTTP/Service banner grabbing |
| `-o` | `--output` | String | *None* | Output file path for exporting results |
| `-f` | `--format` | String | `txt` | Report format (`txt`, `json`, `csv`) |
| `-i` | `--interactive` | Flag | `False` | Launch interactive menu mode |
| `-q` | `--quiz` | Flag | `False` | Launch the educational port quiz |

---

### CLI Examples

1. **Scan default top ports (1-1024) on localhost:**
   ```bash
   python3 main.py -t 127.0.0.1
   ```

2. **Scan specific port range with banner grabbing enabled:**
   ```bash
   python3 main.py -t scanme.nmap.org -p 20-100 -b
   ```

3. **High-speed scan with custom timeout and threads:**
   ```bash
   python3 main.py -t 192.168.1.1 -p 1-10000 --threads 50 --timeout 0.5
   ```

4. **Scan and export directly to a JSON report:**
   ```bash
   python3 main.py -t 127.0.0.1 -p 80-443 -o scan_results.json -f json
   ```

5. **Launch the Educational Quiz directly:**
   ```bash
   python3 main.py --quiz
   ```

6. **Launch Interactive Mode:**
   ```bash
   python3 main.py -i
   # Or run without any arguments:
   python3 main.py
   ```

---

## 🎓 Practice Scenarios & Learning Exercises

### Scenario 1: Local Network Reconnaissance (Lab Environment)
Set up a vulnerable virtual machine (such as Metasploitable2 or DVWA) on a private lab network (e.g., `192.168.56.101`).

1. Run a scan across common administrative ports:
   ```bash
   python3 main.py -t 192.168.56.101 -p 20-110 -b
   ```
2. **Analysis Task:** Identify any plain-text protocols operating on the host (e.g., FTP on port 21, Telnet on port 23, POP3 on port 110) and document their security implications.

### Scenario 2: Web Server Audit
Test an authorized web server target (e.g., `scanme.nmap.org`):

1. Execute a targeted scan on web and management ports:
   ```bash
   python3 main.py -t scanme.nmap.org -p 80-443 -b -o web_audit.csv -f csv
   ```
2. **Analysis Task:** Check the retrieved banners for web server versions (e.g., Apache, Nginx) and compare HTTP vs HTTPS configurations.

### Scenario 3: Test Knowledge with the Quiz
Run the built-in educational module to practice port-to-service mapping and security theory:
```bash
python3 main.py -q
```

---

## 📁 Project Structure

```text
PortScannerPractice/
├── main.py         # Application entry point & execution dispatcher
├── scanner.py      # Core multi-threaded TCP port scanning engine
├── services.py     # Network service database & security implications
├── exporter.py     # Result formatting & export modules (JSON, CSV, TXT)
├── education.py    # Interactive port identification quiz & study module
├── cli.py          # Command-line parser, banner display & interactive menu
└── README.md       # Project documentation & user guide
```

---

## 📄 License

Distributed under the MIT License. Created for educational and ethical cybersecurity practice.
