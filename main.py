import requests
from cloudflare import Cloudflare

client = Cloudflare(
    api_email="<account mail address>",
    api_key="<global API key>",
)

zone_id = "<Domain Zone ID"
record_name = "<name of the record>"

def get_current_content():
    page = client.dns.records.list(
        zone_id=zone_id,
    )
    if page.result[0].name == record_name:
        return page.result[0].id, page.result[0].content

def set_current_ip(dns_record_id, current_cf_ip):
    current_ip = get_public_ip()
    if current_ip != current_cf_ip:
        try:
            record_response = client.dns.records.update(
                dns_record_id=dns_record_id,
                zone_id=zone_id,
                name=record_name,
                ttl=60,
                type="A",
                content=current_ip,
            )
            print(f"Changing the following {record_name} record content to {current_ip}")
        except:
            print("Failed to overwrite the A record")
    else:
        print("No update needed")

def get_public_ip():
    try:
        result = requests.get('https://api.ipify.org').content.decode('utf8')
        return result
    except:
        print("Failed to get the public IP")

def main():
    dns_record_id, current_cf_ip = get_current_content()
    set_current_ip(dns_record_id, current_cf_ip)

if __name__ == "__main__":
    main()