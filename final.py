import os
import subprocess
import whois

# Step 1: Download and convert ODS → CSV
print("[*] Downloading and processing the ODS file...")
download_cmd = (
    "wget -qO websiteregister.ods "
    "https://www.communicatierijk.nl/binaries/communicatierijk/documenten/publicaties/2016/05/26/"
    "websiteregister/websiteregister-rijksoverheid-2025-04-16.ods && "
    "ssconvert websiteregister.ods output.csv 2>/dev/null"
)

if subprocess.call(download_cmd, shell=True) != 0:
    print("[-] Failed to download or convert the file.")
    exit(1)
print("[+] File downloaded and converted.")

# Step 2: Extract unique URLs and domains
print("[*] Extracting URLs and domains...")
subprocess.call("grep -Eo 'https?://[^ ,\"]+' output.csv | sort -u > unique_urls.txt", shell=True)
subprocess.call("grep -Eo 'https?://[^/\"]+' unique_urls.txt | sed -E 's~https?://~~' | sed 's/^www\\.//' | sort -u > domains.txt", shell=True)
print("[+] Domains extracted to domains.txt.")

# Step 3: Whois filtering
input_file = "domains.txt"
output_file = input("Enter output save file name: ").strip()
target_keyword = "Rijksoverheid"

def check_registrar(domain, keyword):
    try:
        w = whois.whois(domain)
        registrar = str(w.registrar or "").strip()
        if keyword.lower() in registrar.lower():
            print(f"[ ✔ ] {domain}: -------→ INSCOPE ASSETS  ({registrar})")
            return True
        else:
            print(f"[ ✘ ] {domain}: -------→ OUT OF SCOPE ({registrar})")
            return False
    except Exception as e:
        print(f"[!] Error checking {domain}: {e}")
        return False

def main():
    try:
        with open(input_file, "r") as infile:
            domains = [line.strip() for line in infile if line.strip()]
    except FileNotFoundError:
        print(f"[!] Input file '{input_file}' not found.")
        return

    with open(output_file, "w") as outfile:
        for domain in domains:
            if check_registrar(domain, target_keyword):
                outfile.write(domain + "\n")

    print(f"\n[✓] Done. Matching domains saved to '{output_file}'.")

if __name__ == "__main__":
    main()
