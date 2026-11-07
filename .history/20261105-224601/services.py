import socket

SERVICES_DB = {
    20: {
        "name": "FTP-DATA",
        "protocol": "TCP",
        "description": "File Transfer Protocol (Data Transfer)",
        "implication": "Unencrypted data channel. Transferred files can be captured via packet sniffing."
    },
    21: {
        "name": "FTP",
        "protocol": "TCP",
        "description": "File Transfer Protocol (Control)",
        "implication": "Transmits credentials in cleartext. High risk of brute-force attacks and credential harvesting."
    },
    22: {
        "name": "SSH",
        "protocol": "TCP",
        "description": "Secure Shell",
        "implication": "Secure remote login. Risk of password brute-forcing if key authentication is not enforced."
    },
    23: {
        "name": "Telnet",
        "protocol": "TCP",
        "description": "Telnet unencrypted text communications",
        "implication": "Legacy protocol. Transmits all data including passwords in cleartext. High security risk."
    },
    25: {
        "name": "SMTP",
        "protocol": "TCP",
        "description": "Simple Mail Transfer Protocol",
        "implication": "Mail server routing. Can be exploited for spam relaying, email spoofing, or user enumeration."
    },
    53: {
        "name": "DNS",
        "protocol": "TCP/UDP",
        "description": "Domain Name System",
        "implication": "Target for DNS cache poisoning, amplification DDoS attacks, and unauthorized zone transfers."
    },
    69: {
        "name": "TFTP",
        "protocol": "UDP",
        "description": "Trivial File Transfer Protocol",
        "implication": "Simple file transfer with no authentication mechanisms. High risk if exposed."
    },
    80: {
        "name": "HTTP",
        "protocol": "TCP",
        "description": "Hypertext Transfer Protocol",
        "implication": "Unencrypted web traffic. Sensitive data transmitted without SSL/TLS can be intercepted."
    },
    88: {
        "name": "Kerberos",
        "protocol": "TCP/UDP",
        "description": "Kerberos Network Authentication",
        "implication": "Active Directory target. Susceptible to Kerberoasting and AS-REP roasting attacks."
    },
    110: {
        "name": "POP3",
        "protocol": "TCP",
        "description": "Post Office Protocol v3",
        "implication": "Retrieves emails in cleartext unless SSL/TLS (995) is used. Passwords can be intercepted."
    },
    123: {
        "name": "NTP",
        "protocol": "UDP",
        "description": "Network Time Protocol",
        "implication": "Clock synchronization. Can be abused for massive UDP reflection/amplification DDoS attacks."
    },
    135: {
        "name": "MS-RPC",
        "protocol": "TCP",
        "description": "Microsoft RPC Endpoint Mapper",
        "implication": "Used for remote administration. Frequently targeted by Windows remote code execution exploits."
    },
    137: {
        "name": "NetBIOS-NS",
        "protocol": "UDP",
        "description": "NetBIOS Name Service",
        "implication": "Legacy Windows naming. Susceptible to LLMNR/NBT-NS spoofing (Responder attacks)."
    },
    139: {
        "name": "NetBIOS-SSN",
        "protocol": "TCP",
        "description": "NetBIOS Session Service",
        "implication": "Used for file/printer sharing. Legacy SMB transport with known security vulnerabilities."
    },
    143: {
        "name": "IMAP",
        "protocol": "TCP",
        "description": "Internet Message Access Protocol",
        "implication": "Unencrypted email access. Transmits credentials in plain text unless IMAPS (993) is used."
    },
    161: {
        "name": "SNMP",
        "protocol": "UDP",
        "description": "Simple Network Management Protocol",
        "implication": "Network device monitoring. Weak default community strings (public/private) leak network topology."
    },
    389: {
        "name": "LDAP",
        "protocol": "TCP/UDP",
        "description": "Lightweight Directory Access Protocol",
        "implication": "Unencrypted directory queries. Exposes Active Directory user and organizational structures."
    },
    443: {
        "name": "HTTPS",
        "protocol": "TCP",
        "description": "HTTP Secure",
        "implication": "Encrypted web traffic. Security risks rely on web app code quality and TLS certificate configuration."
    },
    445: {
        "name": "SMB",
        "protocol": "TCP",
        "description": "Server Message Block",
        "implication": "Windows file sharing. High-value target for lateral movement, ransomware (EternalBlue), and SMB relay."
    },
    465: {
        "name": "SMTPS",
        "protocol": "TCP",
        "description": "Simple Mail Transfer Protocol Secure",
        "implication": "Encrypted email submission. Requires modern TLS ciphers to prevent interception."
    },
    500: {
        "name": "ISAKMP",
        "protocol": "UDP",
        "description": "IPsec Internet Key Exchange",
        "implication": "VPN tunnel setup. Vulnerable to weak pre-shared key (PSK) cracking in aggressive mode."
    },
    514: {
        "name": "Syslog",
        "protocol": "UDP",
        "description": "System Logging Protocol",
        "implication": "Unencrypted log messages. Can leak system activity and event data across the network."
    },
    587: {
        "name": "SMTP-Submission",
        "protocol": "TCP",
        "description": "Message Submission over STARTTLS",
        "implication": "Email submission port. Ensure STARTTLS is enforced to prevent cleartext fallback."
    },
    636: {
        "name": "LDAPS",
        "protocol": "TCP",
        "description": "Lightweight Directory Access Protocol Secure",
        "implication": "Encrypted directory service. Preferred over 389; SSL/TLS validation required."
    },
    853: {
        "name": "DoT",
        "protocol": "TCP",
        "description": "DNS over TLS",
        "implication": "Encrypted DNS queries. Protects user privacy against local DNS sniffing."
    },
    993: {
        "name": "IMAPS",
        "protocol": "TCP",
        "description": "Internet Message Access Protocol Secure",
        "implication": "Encrypted email retrieval. Preferred over port 143."
    },
    995: {
        "name": "POP3S",
        "protocol": "TCP",
        "description": "Post Office Protocol 3 Secure",
        "implication": "Encrypted email retrieval. Preferred over port 110."
    },
    1433: {
        "name": "MSSQL",
        "protocol": "TCP",
        "description": "Microsoft SQL Server",
        "implication": "Database engine. Susceptible to SQL injection, weak SA passwords, and RCE via xp_cmdshell."
    },
    1521: {
        "name": "Oracle-DB",
        "protocol": "TCP",
        "description": "Oracle Database Listener",
        "implication": "Exposed database. Risk of TNS listener exploitation, SID enumeration, and default credentials."
    },
    2049: {
        "name": "NFS",
        "protocol": "TCP/UDP",
        "description": "Network File System",
        "implication": "Network file sharing. Weak root-squashing or no access controls allow unauthorized file access."
    },
    3306: {
        "name": "MySQL",
        "protocol": "TCP",
        "description": "MySQL Database",
        "implication": "Database server. Risk of unauthorized data access, SQL injection, and password brute-forcing."
    },
    3389: {
        "name": "RDP",
        "protocol": "TCP",
        "description": "Remote Desktop Protocol",
        "implication": "Windows GUI remote access. Prime target for brute-force logins and exploits (BlueKeep)."
    },
    5432: {
        "name": "PostgreSQL",
        "protocol": "TCP",
        "description": "PostgreSQL Database",
        "implication": "Relational database server. Vulnerable to weak authentication and remote code execution."
    },
    5900: {
        "name": "VNC",
        "protocol": "TCP",
        "description": "Virtual Network Computing",
        "implication": "Remote desktop access. Often configured with weak or no authentication mechanisms."
    },
    6379: {
        "name": "Redis",
        "protocol": "TCP",
        "description": "Redis Key-Value Store",
        "implication": "In-memory database. Frequently left unauthenticated, enabling arbitrary code execution or SSH key write."
    },
    8080: {
        "name": "HTTP-Proxy",
        "protocol": "TCP",
        "description": "HTTP Alternate / Proxy / Tomcat",
        "implication": "Common alt HTTP port. Often hosts administrative consoles or development web apps."
    },
    8443: {
        "name": "HTTPS-Alt",
        "protocol": "TCP",
        "description": "HTTPS Alternate",
        "implication": "Alternate encrypted web port. Frequently used for web app management interfaces."
    },
    9200: {
        "name": "Elasticsearch",
        "protocol": "TCP",
        "description": "Elasticsearch RESTful API",
        "implication": "Search and analytics engine. Unauthenticated exposure can lead to massive data breaches."
    },
    11211: {
        "name": "Memcached",
        "protocol": "TCP/UDP",
        "description": "Memcached Memory Cache System",
        "implication": "Caching daemon. Vulnerable to UDP amplification DDoS attacks and unauthenticated data theft."
    },
    27017: {
        "name": "MongoDB",
        "protocol": "TCP",
        "description": "MongoDB NoSQL Database",
        "implication": "NoSQL database. Default installations lack authentication, frequently targeted by ransomware."
    }
}


def get_service_info(port: int) -> dict:
    """
    Look up service details by port number.
    Returns a dictionary containing service name, protocol, description, and security implication.
    """
    if port in SERVICES_DB:
        return SERVICES_DB[port]
    
    # Attempt fallback using socket standard library lookup
    try:
        service_name = socket.getservbyport(port)
        return {
            "name": service_name.upper(),
            "protocol": "TCP",
            "description": f"Standard network service on port {port}.",
            "implication": "Uncommon or non-standard port configuration. Assess service banner for potential risks."
        }
    except Exception:
        return {
            "name": "Unknown",
            "protocol": "TCP/UDP",
            "description": "Unregistered or obscure network port.",
            "implication": "Unusual open port. Could indicate custom application, backdoor, or non-standard service configuration."
        }


def get_all_services() -> dict:
    """Return the entire service database."""
    return SERVICES_DB


def get_common_ports() -> list:
    """Return list of common port numbers included in the database."""
    return list(SERVICES_DB.keys())
