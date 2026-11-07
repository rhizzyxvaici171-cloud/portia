import random
import sys

try:
    from services import SERVICES_DB
except ImportError:
    SERVICES_DB = {}


STATIC_QUESTIONS = [
    {
        "question": "Which port is commonly used for secure remote shell access (SSH)?",
        "options": ["21", "22", "23", "80"],
        "answer": "22",
        "explanation": "Port 22 is used by SSH for encrypted remote command-line administration."
    },
    {
        "question": "Why is running Telnet (Port 23) considered a major security risk?",
        "options": [
            "It transmits data and passwords in unencrypted plain text",
            "It uses excessive CPU resources",
            "It requires hardware token authentication",
            "It only accepts IPv6 connections"
        ],
        "answer": "It transmits data and passwords in unencrypted plain text",
        "explanation": "Telnet communicates in cleartext, making credentials vulnerable to network sniffing."
    },
    {
        "question": "Which port is used by DNS (Domain Name System) for domain name resolution?",
        "options": ["53", "67", "123", "161"],
        "answer": "53",
        "explanation": "DNS operates on Port 53 using both UDP and TCP protocols."
    },
    {
        "question": "What is the default port for HTTPS (HTTP Secure)?",
        "options": ["80", "8080", "443", "8443"],
        "answer": "443",
        "explanation": "HTTPS uses port 443 to deliver web traffic encrypted with TLS/SSL."
    },
    {
        "question": "Which attack type frequently targets Kerberos on Port 88 in Active Directory?",
        "options": [
            "Kerberoasting / AS-REP Roasting",
            "SQL Injection",
            "Cross-Site Scripting (XSS)",
            "Buffer Overflow in FTP"
        ],
        "answer": "Kerberoasting / AS-REP Roasting",
        "explanation": "Kerberos (Port 88) ticket requests can be exploited for offline password cracking."
    },
    {
        "question": "FTP uses which port for establishing its control channel?",
        "options": ["20", "21", "22", "25"],
        "answer": "21",
        "explanation": "FTP command sessions open on TCP Port 21, while data transfer uses Port 20."
    },
    {
        "question": "Which unencrypted mail transfer protocol defaults to TCP Port 25?",
        "options": ["POP3", "IMAP", "SMTP", "SNMP"],
        "answer": "SMTP",
        "explanation": "Simple Mail Transfer Protocol (SMTP) uses Port 25 for sending emails between servers."
    }
]


def generate_dynamic_questions():
    questions = []
    if not SERVICES_DB:
        return questions

    ports = list(SERVICES_DB.keys())
    for port in ports:
        info = SERVICES_DB[port]
        name = info.get("name", "Unknown")
        implication = info.get("implication", "N/A")
        description = info.get("description", "")
        
        other_names = [SERVICES_DB[p].get("name", "Unknown") for p in ports if p != port]
        other_names = list(dict.fromkeys(other_names))
        
        if len(other_names) >= 3:
            random.shuffle(other_names)
            wrong_choices = other_names[:3]
            options = wrong_choices + [name]
            random.shuffle(options)
            
            questions.append({
                "question": f"Which network service typically operates on Port {port}?",
                "options": options,
                "answer": name,
                "explanation": f"Port {port} defaults to {name} ({description}). Security risk: {implication}"
            })

    return questions


def display_header(title):
    print("\n" + "=" * 60)
    print(f" {title} ".center(60, "="))
    print("=" * 60)


def run_quiz():
    display_header("Cybersecurity Port Identification Quiz")
    print("Test your knowledge of network ports, protocols, and security implications.\n")

    dynamic_qs = generate_dynamic_questions()
    all_questions = STATIC_QUESTIONS + dynamic_qs
    random.shuffle(all_questions)
    
    quiz_pool = all_questions[:8] if len(all_questions) >= 8 else all_questions

    if not quiz_pool:
        print("[!] No quiz questions available.")
        return

    score = 0
    total = len(quiz_pool)

    for i, q in enumerate(quiz_pool, start=1):
        print(f"Question {i} of {total}:")
        print(f"{q['question']}\n")

        options = q["options"]
        for idx, option in enumerate(options, start=1):
            print(f"  [{idx}] {option}")

        while True:
            try:
                user_input = input("\nYour choice (1-4, or 'q' to quit): ").strip()
                if user_input.lower() == 'q':
                    print("\n[*] Exiting quiz mode...")
                    return
                choice_idx = int(user_input) - 1
                if 0 <= choice_idx < len(options):
                    selected = options[choice_idx]
                    break
                else:
                    print("[!] Please enter a number between 1 and 4.")
            except (ValueError, IndexError):
                print("[!] Invalid input. Please enter a valid number or 'q'.")
            except (KeyboardInterrupt, EOFError):
                print("\n\n[*] Quiz interrupted.")
                return

        if selected == q["answer"]:
            print("\n[+] Correct!")
            score += 1
        else:
            print(f"\n[-] Incorrect. The correct answer was: {q['answer']}")
        
        print(f"    Explanation: {q['explanation']}")
        print("-" * 60 + "\n")

    percentage = (score / total) * 100
    display_header("Quiz Results")
    print(f"Final Score: {score} / {total} ({percentage:.1f}%)")
    
    if percentage == 100:
        print("[*] Outstanding! Perfect understanding of port cybersecurity fundamentals.")
    elif percentage >= 75:
        print("[*] Great job! You have a solid command of networking security.")
    elif percentage >= 50:
        print("[*] Fair result. Review port numbers and risks to sharpen your knowledge.")
    else:
        print("[*] Keep practicing to improve your understanding of port security!")
