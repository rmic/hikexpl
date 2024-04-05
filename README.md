# hikexpl: Exploiting Hikvision Backdoor (CVE-2017-7921)

## Overview
This Python script, named hikexpl, is designed as a poc to demonstrate the the Hikvision backdoor vulnerability, CVE-2017-7921. 
The focus of this script is not only on exploiting the vulnerability but also on writing clean, readable, and maintainable Python code.

## Features
* Scanning: Utilizes the Shodan API to scan for devices vulnerable to CVE-2017-7921 based on user-provided dorks.
* Exploitation: Offers options to exploit the identified vulnerable devices, including taking snapshots and extracting passwords.
* Concurrency: Supports multiple processes to efficiently exploit multiple targets simultaneously.
* Configuration: Allows customization of various parameters such as the output file, snapshot folder, use of Tor for requests (not available yet in Python 3.12), and more.

## Usage

### Installation
1. Clone the repository:
```bash
git clone https://github.com/rmic/hikexpl.git
cd hikexpl
```

2. Install the tool and its dependencies :
```bash
pip install .
```
## Commands

- Version: Display the version of hikexpl.
- Scan: Scan for devices vulnerable to CVE-2017-7921 using Shodan.
```bash
$ hikexp scan --token YOUR_SHODAN_API_TOKEN --dork "YOUR_SHODAN_DORK" --pages NUM_PAGES --output OUTPUT_FILE
```

- Exploit: Exploit the identified vulnerable devices.
```bash
hikexpl exploit --file TARGETS_FILE [--take-snapshots] [--extract-passwords] [--passwords-file PASSWORDS_FILE] [--snapshots-folder SNAPSHOTS_FOLDER] [--use-tor] [--reuse-session] [--process-count PROCESS_COUNT]
```

## Important Note
This tool is for educational purposes only. 
Ensure that you have proper authorization before scanning or exploiting any devices. Misuse of this tool may lead to legal consequences.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
The cybersecurity community for their contributions in identifying and addressing vulnerabilities like CVE-2017-7921.

Authors of the following repos :
- https://github.com/mr-exo/shodan-dorks
- https://github.com/mr-exo/HikvisionBackdoor/
- https://github.com/diego-tella/HikvisionIN/
- https://github.com/JrDw0/CVE-2017-7921-EXP




