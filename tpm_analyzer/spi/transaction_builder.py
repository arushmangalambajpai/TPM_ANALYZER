"""
transaction_builder.py

Convert raw SPI analyzer CSV into
complete SPI transactions.

Input:

Saleae style:

Index appears only at transaction start.

Rows:

Index   MOSI   MISO

0       byte   byte
blank   byte   byte
blank   byte   byte

1       byte   byte


Output:

Index,MOSI,MISO

0,"C0 DE 00 00","00 00 01 FF"
"""


import csv


from tpm_analyzer.utils.byte_utils import (
    bytes_to_hex
)


# =========================================================
# BUILD TRANSACTIONS
# =========================================================


def build_transactions(input_csv):


    transactions = {}


    current_index = None



    with open(
        input_csv,
        newline=""
    ) as file:



        reader = csv.DictReader(
            file
        )



        for row in reader:



            index_value = row["Index"].strip()



            # -----------------------------------------
            # NEW TRANSACTION START
            # -----------------------------------------


            if index_value != "":


                # CSV gives 0.0, 1.0 sometimes

                current_index = str(
                    int(
                        float(index_value)
                    )
                )



                transactions[current_index] = {

                    "mosi": [],

                    "miso": []

                }



            # ignore garbage before first index


            if current_index is None:


                continue



            # -----------------------------------------
            # ADD BYTES
            # -----------------------------------------


            mosi = row["MOSI"].strip()


            miso = row["MISO"].strip()



            if mosi != "":


                transactions[current_index]["mosi"].append(


                    int(
                        mosi,
                        16
                    )

                )



            if miso != "":


                transactions[current_index]["miso"].append(


                    int(
                        miso,
                        16
                    )

                )



    return transactions



# =========================================================
# WRITE TRANSACTION FILE
# =========================================================


def write_transactions(
        transactions,
        output_csv
):


    with open(
        output_csv,
        "w",
        newline=""
    ) as file:


        writer = csv.writer(
            file
        )


        writer.writerow(
            [
                "Index",
                "MOSI",
                "MISO"
            ]
        )



        for index,data in transactions.items():


            writer.writerow(
                [

                    index,


                    bytes_to_hex(
                        data["mosi"]
                    ),


                    bytes_to_hex(
                        data["miso"]
                    )

                ]
            )



# =========================================================
# MAIN API
# =========================================================


def convert_spi_csv(
        input_csv,
        output_csv
):


    transactions = build_transactions(
        input_csv
    )


    write_transactions(
        transactions,
        output_csv
    )


    return len(
        transactions
    )



# =========================================================
# SELF TEST
# =========================================================


if __name__ == "__main__":


    count = convert_spi_csv(


        "rpi_boot_csv.csv",


        "output/spi_transactions.csv"


    )



    print(

        "Transactions generated:",

        count

    )