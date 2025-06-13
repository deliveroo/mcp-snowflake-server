# Certificate Files

## Netskope Certificate

Place your Netskope certificate file as `nscacert.pem` in this directory.

### How to obtain the certificate:

1. Follow the [Netskope / SSL issues with python hitting APIs locally](https://deliveroo.atlassian.net/wiki/spaces/BI/pages/5260050516/Netskope+SSL+issues+with+python+hitting+APIs+locally) guide
2. Download the certificate file
3. Copy it to this directory and rename it to `nscacert.pem`

### Alternative:

If you prefer to keep the certificate elsewhere, you can still use the `NETSKOPE_CERTIFICATE_FILE` environment variable to specify the path to your certificate file. 