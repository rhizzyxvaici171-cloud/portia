import csv
import json
import os
from datetime import datetime


def _format_txt(results):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        "=" * 60,
        "          Port Scanner Practice - Scan Report          ",
        "=" * 60,
        f"Generated on: {timestamp}",
        f"Total open ports found: {len(results)}",
        "-" * 60,
        ""
    ]

    if not results:
        lines.append("No open ports were discovered during this scan.")
    else:
        for item in results:
            lines.append(
                f"Port: {item.get('port')} | Status: {item.get('status', 'open')} | Service: {item.get('service', 'unknown')}"
            )
            lines.append(f"  Security Implication: {item.get('implication', 'N/A')}")
            banner = item.get('banner')
            if banner:
                lines.append(f"  Banner: {banner}")
            lines.append("-" * 40)

    return "\n".join(lines)


def export_json(results, filepath):
    report_data = {
        "timestamp": datetime.now().isoformat(),
        "total_open_ports": len(results),
        "results": results
    }
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(report_data, f, indent=4)


def export_csv(results, filepath):
    fieldnames = ["port", "status", "service", "implication", "banner"]
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for item in results:
            writer.writerow({
                "port": item.get("port", ""),
                "status": item.get("status", "open"),
                "service": item.get("service", "unknown"),
                "implication": item.get("implication", "N/A"),
                "banner": item.get("banner", "") or ""
            })


def export_txt(results, filepath):
    content = _format_txt(results)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)


def export_results(results, filename, fmt="txt"):
    if not filename:
        print("[!] Error: No output filename specified.")
        return False

    fmt = fmt.lower() if fmt else "txt"

    base, ext = os.path.splitext(filename)
    if not ext:
        filename = f"{filename}.{fmt}"
    elif ext.lstrip('.').lower() in ['json', 'csv', 'txt']:
        fmt = ext.lstrip('.').lower()

    try:
        if fmt == 'json':
            export_json(results, filename)
        elif fmt == 'csv':
            export_csv(results, filename)
        else:
            export_txt(results, filename)

        print(f"[+] Scan report successfully saved to '{filename}' (Format: {fmt.upper()})")
        return True
    except Exception as e:
        print(f"[!] Failed to export results to '{filename}': {e}")
        return False
