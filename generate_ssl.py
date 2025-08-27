#!/usr/bin/env python3
"""
Generate SSL certificates if they don't exist
"""
from OpenSSL import crypto
import os
from pathlib import Path

def generate_ssl_cert():
    cert_file = Path("config/ssl/server.crt")
    key_file = Path("config/ssl/server.key")
    
    # Create directories if they don't exist
    cert_file.parent.mkdir(parents=True, exist_ok=True)
    
    if cert_file.exists() and key_file.exists():
        print("SSL certificates already exist.")
        return
    
    # Create a key pair
    key = crypto.PKey()
    key.generate_key(crypto.TYPE_RSA, 2048)
    
    # Create a self-signed cert
    cert = crypto.X509()
    cert.get_subject().CN = "localhost"
    cert.set_serial_number(1000)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(365*24*60*60)
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(key)
    cert.sign(key, 'sha256')
    
    # Save certificate
    with open(cert_file, "wb") as f:
        f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
    
    # Save private key
    with open(key_file, "wb") as f:
        f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, key))
    
    print(f"Generated SSL certificate: {cert_file}")
    print(f"Generated SSL key: {key_file}")

if __name__ == "__main__":
    generate_ssl_cert()