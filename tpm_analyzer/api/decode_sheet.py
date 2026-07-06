"""
decode_sheet.py

Decode reconstructed SPI transaction CSV.

Input:

    output/spi_transactions.csv


Format:

    Index,MOSI,MISO


Output:

    output/decoded_transactions.csv

    output/command_summary.txt


This file does NOT:
- Build SPI transactions from byte CSV
- Print full descriptions

For full decode use:

    decode_full.py
"""


import csv


from tpm_analyzer.spi.header_decoder import (
    decode_spi_header
)


from tpm_analyzer.registers.register_map import (
    get_register
)


from tpm_analyzer.fifo.fifo import (
    is_fifo_stream,
    get_code
)


from tpm_analyzer.tpm.response import (
    get_response_code
)


from tpm_analyzer.utils.byte_utils import (
    bytes_to_hex
)



# =========================================================
# TPM CC NAME
# =========================================================


def get_tpm_cc_name(command_code):


    if command_code is None:

        return ""


    try:


        from tpmstream.spec.structures.constants import (
            TPM_CC
        )


        return str(
            TPM_CC(command_code)
        )


    except Exception:


        return "UNKNOWN"




# =========================================================
# READ TRANSACTION CSV
# =========================================================


def read_transactions(filename):


    transactions = []



    with open(
        filename,
        newline=""
    ) as file:



        reader = csv.DictReader(
            file
        )



        for row in reader:



            mosi = []

            miso = []



            if row["MOSI"].strip():


                for byte in row["MOSI"].split():


                    mosi.append(

                        int(byte,16)

                    )



            if row["MISO"].strip():


                for byte in row["MISO"].split():


                    miso.append(

                        int(byte,16)

                    )



            transactions.append(


                {

                    "index": row["Index"],

                    "mosi": mosi,

                    "miso": miso

                }


            )



    return transactions





# =========================================================
# MOSI ROW
# =========================================================


def decode_mosi_summary(
        index,
        mosi
):


    row = empty_row(
        index,
        "MOSI"
    )



    try:


        header = decode_spi_header(
            mosi
        )


    except Exception:


        return row,None,None



    register = get_register(

        header["register_offset"]

    )


    payload = header["payload"]



    fill_common(

        row,

        header,

        register,

        payload

    )



    command_code = None



    if register in [

        "TPM_DATA_FIFO",

        "TPM_X_DATA_FIFO"

    ]:


        if is_fifo_stream(payload):


            command_code = get_code(
                payload
            )


            row["TPM_CC"] = (

                f"{command_code:08X}"

            )


            row["TPM_CC_NAME"] = (

                get_tpm_cc_name(
                    command_code
                )

            )



    return row,header,command_code





# =========================================================
# MISO ROW
# =========================================================


def decode_miso_summary(
        index,
        miso,
        header,
        last_command
):


    row = empty_row(
        index,
        "MISO"
    )



    if header is None:


        row["RegisterPayload"] = bytes_to_hex(
            miso
        )


        return row



    register = get_register(

        header["register_offset"]

    )



    # MISO data appears after SPI header clocks


    if header["operation"] == "READ":


        size = header["transfer_size"]


        payload = miso[-size:]


    else:


        payload = []



    fill_common(

        row,

        header,

        register,

        payload

    )



    if register in [

        "TPM_DATA_FIFO",

        "TPM_X_DATA_FIFO"

    ]:


        if is_fifo_stream(payload):


            response_code = get_response_code(

                payload

            )



            if response_code is not None:


                row["TPM_CC"] = (

                    f"Response:{response_code:08X}"

                )



            if last_command:


                row["TPM_CC_NAME"] = (


                    get_tpm_cc_name(

                        last_command

                    )

                    + " Response"

                )



    return row





# =========================================================
# ROW HELPERS
# =========================================================


def empty_row(index,side):


    return {


        "Index": index,


        "Type": side,


        "OperationType": "",


        "Size(bytes)": "",


        "Locality": "",


        "RegisterAddr": "",


        "RegisterName": "",


        "RegisterPayload": "",


        "TPM_CC": "",


        "TPM_CC_NAME": ""

    }





def fill_common(
        row,
        header,
        register,
        payload
):


    row["OperationType"] = (

        header["operation"]

    )


    row["Size(bytes)"] = (

        len(payload)

    )


    row["Locality"] = (

        header["locality"]

    )


    row["RegisterAddr"] = (

        header["register_offset"]

    )


    row["RegisterName"] = register



    row["RegisterPayload"] = (

        bytes_to_hex(payload)

    )





# =========================================================
# OUTPUT FILES
# =========================================================


def write_csv(
        rows,
        filename
):


    headers = list(

        rows[0].keys()

    )



    with open(
        filename,
        "w",
        newline=""
    ) as file:



        writer = csv.DictWriter(

            file,

            headers

        )


        writer.writeheader()



        writer.writerows(

            rows

        )





def write_summary(
        rows,
        filename
):


    summary = {}



    for row in rows:



        name = row["TPM_CC_NAME"]



        if (
            name == ""
            or "Response" in name
        ):


            continue



        if name not in summary:


            summary[name] = []



        summary[name].append(

            row["Index"]

        )



    with open(
        filename,
        "w"
    ) as file:



        file.write(

            "TPM COMMAND SUMMARY\n"

        )


        file.write(

            "====================\n\n"

        )



        for name,indexes in summary.items():



            file.write(

                name + "\n"

            )



            file.write(

                "Count : "

                + str(len(indexes))

                + "\n"


            )



            file.write(

                "Indexes : "

                + ", ".join(indexes)

                + "\n\n"

            )



    return summary





# =========================================================
# MAIN API
# =========================================================


def decode_sheet(
        input_csv,
        output_csv,
        summary_file
):


    transactions = read_transactions(

        input_csv

    )



    rows = []



    last_command = None



    for transaction in transactions:



        mosi_row,header,command = decode_mosi_summary(


            transaction["index"],


            transaction["mosi"]


        )



        rows.append(

            mosi_row

        )



        if command is not None:


            last_command = command




        miso_row = decode_miso_summary(


            transaction["index"],


            transaction["miso"],


            header,


            last_command


        )



        rows.append(

            miso_row

        )



    write_csv(

        rows,

        output_csv

    )



    summary = write_summary(

        rows,

        summary_file

    )



    return {


        "transactions":

            len(transactions),



        "commands":

            summary

    }





# =========================================================
# TEST
# =========================================================


if __name__ == "__main__":



    result = decode_sheet(


        "output/spi_transactions.csv",


        "output/decoded_transactions.csv",


        "output/command_summary.txt"


    )



    print(

        "Decoded Transactions:",

        result["transactions"]

    )



    print()



    for name,indexes in result["commands"].items():


        print(

            name,

            ":",

            len(indexes)

        )