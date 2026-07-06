"""
pcr_extend.py

TPM PCR_Extend Analyzer.

Purpose:

Find TPM_CC.PCR_Extend commands
and extract:

- Transaction Index
- PCR Number
- Hash Algorithm
- Digest


Input:

    output/decoded_transactions.csv


Output:

    output/pcr_extend_report.csv


This file uses:

decoded sheet
        |
        |
TPM command payload
        |
        |
tpmstream decoder
        |
        |
parse human tree output
"""


import csv
import re


from tpm_analyzer.tpm.command import (
    decode_tpm_command
)


from tpm_analyzer.utils.byte_utils import (
    hex_to_bytes
)




# =========================================================
# PARSE TPMSTREAM PCR EXTEND OUTPUT
# =========================================================
def parse_pcr_extend_text(text):

    """
    Extract PCR Extend fields
    from tpmstream decoded output.
    """
        # Remove terminal color escape sequences

    text = re.sub(
        r"\x1b\[[0-9;]*m",
        "",
        text
    )

    result = {

        "PCR": "",

        "HashAlgorithm": "",

        "Digest": ""

    }



    lines = text.splitlines()



    for line in lines:


        parts = line.split()



        # ------------------------------------------
        # PCR HANDLE
        # ------------------------------------------


        if ".pcrHandle" in line:


            for item in parts:


                if "PCR." in item:


                    result["PCR"] = (

                        item.split(".")[-1]

                    )



        # ------------------------------------------
        # HASH ALGORITHM
        # ------------------------------------------


        if ".hashAlg" in line:


            for item in parts:


                if "HASH." in item:


                    result["HashAlgorithm"] = (

                        item.split(".")[-1]

                    )



        # ------------------------------------------
        # DIGEST
        # ------------------------------------------

        # ------------------------------------------
        # DIGEST
        # ------------------------------------------


        if (
            ".sha1" in line
            or ".sha256" in line
            or ".sha384" in line
            or ".sha512" in line
        ):


            parts = line.split()


            for item in parts:


                clean = item.strip()


                if (

                    len(clean) in [

                        40,     # SHA1

                        64,     # SHA256

                        96,     # SHA384

                        128     # SHA512

                    ]

                    and all(

                        c in "0123456789abcdefABCDEF"

                        for c in clean

                    )

                ):


                    result["Digest"] = clean


                    break


    print(result)
    return result





# =========================================================
# ANALYZE CSV
# =========================================================


def analyze_pcr_extend(
        input_csv,
        output_csv
):


    results = []



    with open(
        input_csv,
        newline=""
    ) as file:



        reader = csv.DictReader(
            file
        )



        for row in reader:



            # only commands


            if row["TPM_CC_NAME"] != "TPM_CC.PCR_Extend":


                continue



            payload_hex = row["RegisterPayload"]



            if payload_hex == "":


                continue



            payload = hex_to_bytes(

                payload_hex

            )



            decoded = decode_tpm_command(

                payload

            )



            parsed = parse_pcr_extend_text(

                decoded["decoded"]

            )



            results.append(


                {


                    "Index":

                        row["Index"],



                    "PCR":

                        parsed["PCR"],



                    "HashAlgorithm":

                        parsed["HashAlgorithm"],



                    "Digest":

                        parsed["Digest"]

                }


            )



    write_report(

        results,

        output_csv

    )



    return results





# =========================================================
# WRITE REPORT
# =========================================================


# =========================================================
# WRITE TEXT REPORT
# =========================================================


def write_report(
        rows,
        filename
):


    with open(
        filename,
        "w"
    ) as file:


        file.write(
            "TPM PCR EXTEND ANALYSIS\n"
        )


        file.write(
            "=======================\n\n\n"
        )



        count = 1



        for row in rows:



            file.write(

                f"PCR Extend #{count}\n\n"

            )



            file.write(

                "Transaction Index : "

                + row["Index"]

                + "\n\n"

            )



            file.write(

                "PCR Extended      : PCR "

                + row["PCR"]

                + "\n\n"

            )



            file.write(

                "Hash Algorithm    : "

                + row["HashAlgorithm"]

                + "\n\n"

            )



            file.write(

                "Digest:\n\n"

            )



            file.write(

                row["Digest"]

                + "\n\n"

            )



            file.write(

                "-" * 60

                + "\n\n"

            )



            count += 1




# =========================================================
# SELF TEST
# =========================================================

# =========================================================
# SELF TEST
# =========================================================


if __name__ == "__main__":



    results = analyze_pcr_extend(


        "output/decoded_transactions.csv",


        "output/pcr_extend_report.txt"


    )



    print(

        "PCR Extend Commands:",

        len(results)

    )



    print()



    for item in results:


        print(

            "Index:",

            item["Index"]

        )


        print(

            "PCR:",

            item["PCR"]

        )


        print(

            "Hash:",

            item["HashAlgorithm"]

        )


        print(

            "Digest:",

            item["Digest"]

        )


        print(

            "-" * 40

        )