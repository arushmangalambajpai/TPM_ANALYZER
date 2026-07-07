"""
web_runner.py

Browser GUI wrapper around TPM Analyzer CLI.

Provides:
A. SPI MOSI Decode
B. Complete SPI Transaction Decode
C. CSV Analyzer
D. TPM FIFO Command Decode
"""


import os
import traceback
import csv


# =====================================================
# CORE IMPORTS
# =====================================================


from tpm_analyzer.api.decode_mosi import (
    decode_mosi
)


from tpm_analyzer.api.decode_full import (
    decode_full
)


from tpm_analyzer.spi.transaction_builder import (
    convert_spi_csv
)


from tpm_analyzer.api.decode_sheet import (
    decode_sheet
)


from tpm_analyzer.analyzers.pcr_extend import (
    analyze_pcr_extend
)


from tpm_analyzer.tpm.command import (
    decode_tpm_command
)


from tpm_analyzer.utils.byte_utils import (
    hex_to_bytes
)



# =====================================================
# PATHS
# =====================================================


INPUT_CSV = (
    "input.csv"
)


SPI_CSV = (
    "output/spi_transactions.csv"
)


DECODED_CSV = (
    "output/decoded_transactions.csv"
)


COMMAND_TXT = (
    "output/command_summary.txt"
)


PCR_TXT = (
    "output/pcr_extend_report.txt"
)



# =====================================================
# HELPERS
# =====================================================


def prepare():


    if not os.path.exists(
        "output"
    ):


        os.mkdir(
            "output"
        )




def ensure_transactions():


    prepare()


    if not os.path.exists(
        SPI_CSV
    ):


        convert_spi_csv(

            INPUT_CSV,

            SPI_CSV

        )




def ensure_decoded():


    ensure_transactions()


    if not os.path.exists(
        DECODED_CSV
    ):


        decode_sheet(

            SPI_CSV,

            DECODED_CSV,

            COMMAND_TXT

        )



# =====================================================
# OPTION A : SPI MOSI
# =====================================================


def web_mosi(data):


    try:


        return str(

            decode_mosi(

                data

            )

        )



    except Exception:


        return traceback.format_exc()



# =====================================================
# OPTION B : COMPLETE TRANSACTION
# =====================================================


def web_full(
        mosi,
        miso
):


    try:


        result = decode_full(

            mosi,

            miso

        )



        return result[

            "text"

        ]



    except Exception:


        return traceback.format_exc()



# =====================================================
# FIFO TPM COMMAND DECODE
# =====================================================


def web_tpm_command(
        payload
):


    try:


        data = hex_to_bytes(

            payload

        )



        decoded = decode_tpm_command(

            data

        )



        return decoded[

            "decoded"

        ]



    except Exception:


        return traceback.format_exc()



# =====================================================
# CSV LOAD
# =====================================================


def web_load_csv(
        text
):


    try:


        prepare()



        with open(

            INPUT_CSV,

            "w",

            encoding="utf-8"

        ) as file:


            file.write(

                text

            )



        # remove old results

        for file in [

            SPI_CSV,

            DECODED_CSV,

            COMMAND_TXT,

            PCR_TXT

        ]:


            if os.path.exists(

                file

            ):


                os.remove(

                    file

                )



        return (

            "CSV Loaded Successfully\n\n"

            "Choose Analysis Option."

        )



    except Exception:


        return traceback.format_exc()



# =====================================================
# CSV OPTION 1
# GET SPI TRANSACTIONS
# =====================================================


def web_transactions():


    try:


        count = convert_spi_csv(

            INPUT_CSV,

            SPI_CSV

        )



        return (

            "SPI Transactions Generated\n\n"

            +

            "Transactions : "

            +

            str(

                count

            )

        )



    except Exception:


        return traceback.format_exc()



# =====================================================
# CSV OPTION 2
# DECODE TRANSACTIONS
# =====================================================


def web_decode_sheet():


    try:


        ensure_decoded()



        return (

            "Decoded Transaction CSV Generated"

        )



    except Exception:


        return traceback.format_exc()



# =====================================================
# CSV OPTION 3
# COMMAND SUMMARY
# =====================================================


def web_commands():


    try:


        ensure_decoded()



        with open(

            COMMAND_TXT

        ) as file:



            return file.read()



    except Exception:


        return traceback.format_exc()



# =====================================================
# CSV OPTION 4
# PCR EXTEND REPORT
# =====================================================


def web_pcr():


    try:


        ensure_decoded()



        rows = analyze_pcr_extend(

            DECODED_CSV,

            PCR_TXT

        )



        with open(

            PCR_TXT

        ) as file:


            report = file.read()



        return (

            "PCR Extend Count : "

            +

            str(

                len(rows)

            )

            +

            "\n\n"

            +

            report

        )



    except Exception:


        return traceback.format_exc()
    
# =====================================================
# CSV OPTION 3
# SINGLE TRANSACTION FULL DECODE
# =====================================================


def web_single_transaction(
        index
):


    try:


        ensure_decoded()



        with open(

            DECODED_CSV,

            newline=""

        ) as file:


            reader = csv.DictReader(

                file

            )



            for row in reader:



                if str(row["Index"]) != str(index):


                    continue




                output = ""



                output += (

                    "TRANSACTION INDEX : "

                    +

                    str(index)

                    +

                    "\n\n"

                )



                output += (

                    "REGISTER DECODE\n"

                    "====================\n\n"

                )



                output += (

                    "Register : "

                    +

                    row["RegisterName"]

                    +

                    "\n\n"

                )



                output += (

                    "Payload:\n"

                    +

                    row["RegisterPayload"]

                    +

                    "\n\n"

                )



                # -------------------------------
                # FIFO COMMAND EXTRA DECODE
                # -------------------------------


                if (

                    row["RegisterName"]

                    ==

                    "TPM_DATA_FIFO"

                    and

                    row["RegisterPayload"]

                    != ""

                ):



                    output += (

                        "\n\nTPM COMMAND DECODE\n"

                        "====================\n\n"

                    )



                    payload = hex_to_bytes(

                        row["RegisterPayload"]

                    )



                    decoded = decode_tpm_command(

                        payload

                    )



                    output += decoded["decoded"]



                return output




        return (

            "Transaction index not found"

        )



    except Exception:


        return traceback.format_exc()