# Hardware-Bound Certificate Generation Prototype

This README outlines the architectural changes and core logic implemented for the certificate generation prototype. These changes allow OpenWISP to automatically generate unique X.509 certificates for devices following the templating structure decoupling from VPN Client.

---

## Overview of Changes

The prototype introduces a new certificate template type that automates the generation of standalone certificates, moving away from the previous limitation where such automation was exclusively reserved for VPN clients.

---

## 1. Template Architecture Decoupling

We modified the `Template` model to support a standalone `cert` type. This includes:

- Adding `cert` to `TYPE_CHOICES`.
- Overriding the `clean()` method to allow `auto_cert=True` for the `cert` type, even if the configuration JSON is empty.
- Allowing the `ca` field to be required for this type to ensure a valid issuer is always present.

---

## How It Works: The Lifecycle

The system uses an asynchronous, signal-driven architecture to handle the heavy lifting of cryptographic generation without slowing down the web interface.

---

## 2. Signal-Driven Generation

We utilized the `m2m_changed` signal on the device-template relationship.

### Trigger

When a `cert` template is assigned to a device, the signal fires.

### Asynchronous Task

A Celery task is dispatched to generate the keys in the background.

### Hardware Binding

The generator:

- Fetches the device's MAC address and UUID.
- Injects these identifiers into the certificate using a custom Private OID (`1.3.6.1.4.1.99999.1`).

---

## 3. Upstream Cryptography Patch

To support hardware binding, a patch was designed for the `_add_extensions` logic in the `django-x509` engine.

- A `try...except` block catches numerical OID strings.
- These are wrapped in a `cryptography.x509.UnrecognizedExtension` object.

This allows us to store unique hardware identifiers directly inside the certificate binary.

---

# Core File Modifications

Below is a summary of the primary file-level changes:

| File                      | Change Description                                                                                                    |
| ------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| `config/base/template.py` | Added `cert` type and updated `clean()` validation to allow `auto_cert` without requiring VPN configurations.         |
| `config/base/config.py`   | Implemented `m2m_changed` signal logic to trigger certificate lifecycle tasks when templates are assigned or removed. |
| `config/tasks.py`         | Created Celery tasks for background RSA/ECDSA key generation and certificate revocation.                              |
| `config/admin.py`         | Updated the Django Admin UI to support the new `cert` template fields and related views.                              |
| `config/apps.py`          | Configured app initialization to safely register signals.                                                             |

---

## Results

Once the background task completes:

- A new certificate is generated.
- The certificate is linked to the device.
- The unique hardware fingerprint is encoded in the certificate extensions.

- New Certificate option in template type
  <img width="894" height="969" alt="image" src="https://github.com/user-attachments/assets/3860680e-20d6-4f53-95b5-635a7b9aac61" />

- Toast notification after assigning that template to a device
  <img width="908" height="970" alt="image" src="https://github.com/user-attachments/assets/aa7f0029-b057-4ee6-91bb-294f40ea3b79" />

- Certificate generatin and MAC address in certificate extension
  <img width="888" height="960" alt="image" src="https://github.com/user-attachments/assets/d9e6cc40-ba45-4c5c-bed0-5f5ea3fcbaed" />

DEMO: 

---

## Key Features Verified

- **Non-blocking UI**: Cryptographic operations are handled by Celery workers.
- **No Schema Changes**: Custom OIDs are stored in the existing `extensions` JSON field.
- **Automatic Revocation**: When the template is unassigned, the certificate is automatically flagged as revoked in the database.
