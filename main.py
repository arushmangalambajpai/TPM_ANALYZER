"""
main.py

TPM SPI LOG DECODER

CLI Application Layer


Made by:
Arush Mangalam Bajpai


This file only connects modules.

It does NOT:
- Decode SPI
- Decode TPM
- Parse registers
"""


import os


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




# =========================================================
# UI HELPERS
# =========================================================


def clear():


    os.system(
        "cls"
    )




def line():


    print(
        "=" * 60
    )




def title():


    clear()


    line()


    print(
        "              TPM SPI LOG DECODER"
    )


    print()


    print(
        "          Made by Arush Mangalam Bajpai"
    )


    line()


    print()





def pause():


    input(
        "\nPress ENTER to continue..."
    )





# =========================================================
# OPTION A
# =========================================================


def single_mosi():


    title()


    print(
        "SPI MOSI TRANSACTION DECODER"
    )


    print(
        """
This mode decodes one SPI MOSI transaction.

Useful for:
- TPM register writes
- TPM FIFO commands

Input format:

80 D4 00 18 40
"""
    )



    data = input(

        "Enter MOSI bytes:\n> "

    )



    print()


    result = decode_mosi(

        data

    )


    print(

        result

    )


    pause()





# =========================================================
# OPTION B
# =========================================================


def complete_transaction():


    title()


    print(
        "COMPLETE SPI TRANSACTION DECODER"
    )


    print(
        """
This mode decodes a complete TPM SPI transfer.

Uses:

MOSI:
    - SPI header
    - Write data

MISO:
    - TPM read responses


Example:

MOSI:
80 D4 00 18 00

MISO:
00 00 00 00 C0
"""
    )



    mosi = input(

        "Enter MOSI bytes:\n> "

    )


    print()


    miso = input(

        "Enter MISO bytes:\n> "

    )



    result = decode_full(

        mosi,

        miso

    )



    print(
        result["text"]
    )



    pause()





# =========================================================
# CSV MENU
# =========================================================


def csv_menu():


    title()


    print(
        "SPI LOG CSV ANALYZER"
    )


    print(
        """
This mode analyzes complete SPI captures.

Flow:

Raw CSV
   |
   |-- Build SPI transactions
   |
   |-- Decode registers
   |
   |-- Decode TPM commands
   |
   |-- Analyze PCR Extend measurements
"""
    )



    csv_path = input(

        "Enter CSV path:\n> "

    )



    transaction_file = (

        "output/spi_transactions.csv"

    )


    decoded_file = (

        "output/decoded_transactions.csv"

    )


    summary_file = (

        "output/command_summary.txt"

    )


    pcr_file = (

        "output/pcr_extend_report.txt"

    )



    while True:


        title()



        print(
            "CSV OPTIONS\n"
        )



        print(
            "1. Get SPI Transactions"
        )


        print(
            "   Join SPI bytes into MOSI/MISO transactions\n"
        )



        print(
            "2. Generate decoded_transactions.csv"
        )


        print(
            "   Decode SPI headers, registers and TPM commands\n"
        )



        print(
            "3. Decode one transaction"
        )


        print(
            "   Enter index and get full explanation\n"
        )



        print(
            "4. TPM Command Summary"
        )


        print(
            "   Count commands and show indexes\n"
        )



        print(
            "5. PCR Extend Analysis"
        )


        print(
            "   Show PCR numbers and measured digests\n"
        )



        print(
            "6. Add new CSV\n"
        )



        print(
            "0. Back\n"
        )



        choice=input(

            "> "

        )



        # ----------------------------------------
        # TRANSACTION BUILDER
        # ----------------------------------------


        if choice=="1":


            count=convert_spi_csv(

                csv_path,

                transaction_file

            )


            print(

                "\nTransactions generated:",

                count

            )


            print(

                "Saved:",

                transaction_file

            )


            pause()



        # ----------------------------------------
        # SHEET DECODER
        # ----------------------------------------


        elif choice=="2":



            result=decode_sheet(

                transaction_file,

                decoded_file,

                summary_file

            )


            print(

                "Decoded:",

                result["transactions"]

            )


            print(

                "Saved:",

                decoded_file

            )


            pause()



        # ----------------------------------------
        # SINGLE INDEX
        # ----------------------------------------


        elif choice=="3":


            decode_index(

                transaction_file

            )



        # ----------------------------------------
        # COMMAND SUMMARY
        # ----------------------------------------


        elif choice=="4":


            if os.path.exists(

                summary_file

            ):


                with open(summary_file) as f:


                    print(

                        f.read()

                    )


            else:


                print(

                    "Generate decoded CSV first."

                )


            pause()



        # ----------------------------------------
        # PCR ANALYZER
        # ----------------------------------------


        elif choice=="5":



            results=analyze_pcr_extend(

                decoded_file,

                pcr_file

            )


            print(

                "PCR Extend Commands:",

                len(results)

            )


            print(

                "Saved:",

                pcr_file

            )


            pause()



        elif choice=="6":


            csv_path=input(

                "New CSV path:\n> "

            )



        elif choice=="0":


            break





# =========================================================
# TRANSACTION BY INDEX
# =========================================================


def decode_index(

        transaction_file

):


    import csv


    wanted=input(

        "Enter transaction index:\n> "

    )


    with open(

        transaction_file,

        newline=""

    ) as file:



        reader=csv.DictReader(file)



        for row in reader:



            if row["Index"]==wanted:



                result=decode_full(

                    row["MOSI"],

                    row["MISO"]

                )


                print(

                    result["text"]

                )


                pause()


                return



    print(

        "Index not found."

    )


    pause()





# =========================================================
# MAIN MENU
# =========================================================


def main():


    while True:


        title()



        print(
"""
Select Input Type:


1. SPI MOSI Transaction

   Decode a single MOSI stream.


2. SPI Complete Transaction

   Decode MOSI + MISO pair.


3. SPI Logs (.csv)

   Analyze complete TPM SPI capture.


0. Exit
"""
        )



        choice=input("> ")



        if choice=="1":


            single_mosi()



        elif choice=="2":


            complete_transaction()



        elif choice=="3":


            csv_menu()



        elif choice=="0":


            break





if __name__=="__main__":


    main()