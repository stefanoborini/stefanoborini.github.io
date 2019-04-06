---
category: microsoft
---

# Signing applications for windows

These notes were made in 2013. They may now be outdated.

## create a certificate request with openssl

```
req -out CSR.csr -new -newkey rsa:2048 -nodes -keyout privateKey.key
```

Enter Distinguished Name information:

- Country: Code The two-letter International Organization for Standardization (ISO) format country code for where your organization is legally registered.
- State/Province: Name of state or province where your organization is located
- Locality: Name of the city in which your organization is registered/located
- Organization: Name The full legal name of your organization.
- Organizational Unit: Optional.
- Common Name: The full legal name of your organization.
- Email Address: Your email address.

Move CSR.csr and privateKey.key to your desktop.

Send the CSR to godaddy, wait two weeks until they ask you for some company related certification.

You get the certificate as a .pem or a .spc. Save these files and the private key, these are important. keep them safe.

The key generated with openssl is in the wrong format. Convert it into the proper format using the pvk 
program http://www.drh-consultancy.demon.co.uk/pvk.html

```
pvk.exe -in privateKey.key -topvk -nocrypt -strong -out private.pvk
```

now use pvk2pfx to convert 

```
pvk2pfx.exe -pvk private.pvk -spc spcfile.spc -pfx certificate.pfx
```

## Signing your application

Now you can use this certificate with signtool

```
signtool sign /f certificate.pfx /t http://tsa.starfieldtech.com /d "project name" /du http://yourcompany.example.com/ code.exe
```


