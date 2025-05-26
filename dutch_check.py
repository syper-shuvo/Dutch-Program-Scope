import whois

# Configuration
input_file = input("Eneter Domain file Name: ").strip()
output_file = input("Enter Output Save File Name : ").strip()
target_keyword = "Rijksoverheid"

def check_registrar(domain, keyword):
    try:
        w = whois.whois(domain)
        registrar = str(w.registrar or "").strip()
        if keyword.lower() in registrar.lower():
            print(f"[ ✔ ] {domain}: -------→ INSCOPE ASSETS  {registrar}")
            return True
        else:
            print(f"[ ✘ ] {domain}: -------→ OUT OF SCOPE {registrar}")
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
