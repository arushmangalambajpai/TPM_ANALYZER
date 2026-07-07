# TPM SPI Log Decoder

**A hardware security analysis platform for decoding Trusted Platform Module (TPM 2.0) SPI communication logs.**

Created by  
**Arush Mangalam Bajpai**

---

## Overview

TPM SPI Log Decoder is a tool designed to analyze the low-level communication between a host processor and a TPM 2.0 device.

It reconstructs raw SPI traffic, decodes TPM FIFO register transactions, interprets TPM command streams, and extracts security-relevant information such as PCR extension operations.

The project was developed while studying the TPM-based Chain of Trust implementation on embedded systems.

The analyzer supports:

- Individual SPI MOSI transactions
- Complete MOSI/MISO SPI exchanges
- Full SPI logic analyzer CSV logs
- TPM FIFO command decoding
- PCR Extend analysis with digest extraction

---

# Online Web Version

The analyzer is available as a fully client-side web application using Pyodide.

No server is required.

The complete Python TPM analyzer runs inside the browser.

Website:

```
https://arushmangalambajpai.github.io/TPM_ANALYZER/
```

Features available online:

- Decode SPI MOSI transactions
- Decode complete SPI communication
- Upload SPI CSV logs
- Generate reconstructed TPM transactions
- Decode TPM commands
- Extract PCR Extend operations
- Download generated analysis files

---

# Why this tool?

During TPM measured boot, commands are exchanged over SPI between the processor and TPM.

A raw SPI capture contains bytes such as:

```
80 D4 00 24 80 01 00 00 00 16 ...
```

Understanding this requires decoding multiple layers:

```
Raw SPI Capture

        ↓

TPM SPI Transaction

        ↓

TPM FIFO Register Layer

        ↓

TPM Command / Response Layer

        ↓

Security Interpretation
(PCR Extend, Capability Query, Startup, etc.)
```

This tool automates that process.

---

# Features

## TPM SPI Register Decoder

Decodes TPM FIFO interface registers:

Examples:

- TPM_ACCESS
- TPM_STS
- TPM_DATA_FIFO
- TPM_DID_VID
- TPM_RID
- TPM_INTERFACE_ID

Example output:

```
Register : TPM_STS

Bit [7] stsValid = 1
TPM_STS register fields are valid

Bit [4] dataAvail = 1
TPM response data available
```

---

## TPM Command Decoder

FIFO payloads are decoded into TPM 2.0 structures.

Example:

```
TPM_CC.GetCapability

TPM_CAP:
    PCRS

propertyCount:
    1
```

Supported using TPM structure decoding through tpmstream.

---

## PCR Extend Analyzer

Automatically detects:

```
TPM_CC.PCR_Extend
```

and extracts:

```
Transaction Index

PCR Number

Hash Algorithm

Digest Value
```

Example:

```
PCR Extended : PCR 07

Hash Algorithm : SHA256

Digest:

AF42E9....
```

---

# Project Structure

```
TPM_ANALYZER

│
├── main.py
│
├── tpm_analyzer/
│
│   ├── spi/
│   │       SPI reconstruction
│   │
│   ├── registers/
│   │       TPM register decoding
│   │
│   ├── tpm/
│   │       TPM command decoding
│   │
│   ├── analyzers/
│   │       PCR analysis tools
│   │
│   └── api/
│           CLI/Web interfaces
│
│
├── docs/
│
│   └── Web interface
│
└── output/
        Generated analysis files
```

---

# Installation (CLI)

## 1. Clone repository

```bash
git clone https://github.com/arushmangalambajpai/TPM_ANALYZER.git

cd YOUR_REPOSITORY
```

---

## 2. Create Python environment

Windows:

```powershell
python -m venv .venv

.venv\Scripts\activate
```

Linux:

```bash
python3 -m venv .venv

source .venv/bin/activate
```

---

## 3. Install requirements

```bash
pip install -r requirements.txt
```

---

# Running CLI Version

Start:

```bash
python main.py
```

You will see:

```
================================

TPM SPI LOG DECODER

Made by Arush Mangalam Bajpai

================================


Select Input Type:

1. SPI MOSI Transaction

2. Complete SPI Transaction

3. SPI CSV Logs
```

---

# Usage

## Option 1: Decode MOSI Transaction

Input:

```
80 DE 00 18 00
```

Output:

```
Operation:
READ

Register:
TPM_STS

Decoded bit fields...
```

---

## Option 2: Decode Complete Transaction

Provide:

```
MOSI Bytes

MISO Bytes
```

The analyzer provides:

- SPI operation
- Register access
- TPM response decoding

---

## Option 3: Analyze SPI CSV Logs

Input:

Logic analyzer CSV capture.

Available operations:

```
1. Generate SPI Transactions

2. Generate Decoded Transactions CSV

3. Decode Transaction by Index

4. TPM Command Count + Index List

5. PCR Extend Report
```

---

# Generated Files

After CSV analysis:

```
output/

├── spi_transactions.csv

├── decoded_transactions.csv

├── command_summary.txt

└── pcr_extend_report.txt
```

---

# Web Version Architecture

The website uses:

```
Browser

   |
   |
   v

Pyodide (Python WASM)

   |
   |
   v

TPM Analyzer Engine

   |
   |
   v

Decoded Results
```

Everything runs locally inside the browser.

No uploaded TPM logs are sent to a server.

---

# References

Based on:

- Trusted Computing Group TPM 2.0 Library Specification

- TCG PC Client Platform TPM Profile (PTP) Specification

- TPM 2.0 FIFO Interface

- tpmstream TPM decoder by Joholl

---

# Applications

Useful for:

- Embedded security research
- TPM communication analysis
- Secure boot debugging
- Measured boot analysis
- Hardware security education

---

# Author

**Arush Mangalam Bajpai**

Electrical and Electronics Engineering  
BITS Pilani

---
# License

This project is released under the MIT License.

See:

- LICENSE
- THIRD_PARTY_LICENSES.md

for details.

Third-party components retain their original licenses.