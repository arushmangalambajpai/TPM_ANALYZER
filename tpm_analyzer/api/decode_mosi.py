"""
decode_mosi.py

Main MOSI Transaction Decoder.

This is a public API file.

It combines:

SPI Header Decoder

        +

Register Decoder

        +

FIFO Command Decoder


Input:

    Complete MOSI SPI transaction


Example:

    80 D4 00 18 C0


Output:

    Human readable TPM explanation


This file does NOT:
- Decode MISO responses
- Decode CSV files
"""


from tpm_analyzer.spi.header_decoder import (
    decode_spi_header,
    format_spi_header
)


from tpm_analyzer.registers.register_map import (
    get_register
)


from tpm_analyzer.registers.register_decoder import (
    decode_register
)


from tpm_analyzer.fifo.fifo import (
    is_fifo_stream
)


from tpm_analyzer.tpm.command import (
    decode_tpm_command
)


from tpm_analyzer.utils.byte_utils import (
    hex_to_bytes
)



# =========================================================
# MOSI DECODER
# =========================================================


def decode_mosi(transaction):

    """
    Decode a MOSI SPI transaction.


    Input:

        hex string

            OR

        byte list


    Output:

        decoded string
    """



    # -----------------------------------------------------
    # Convert input
    # -----------------------------------------------------


    if isinstance(transaction, str):


        transaction = hex_to_bytes(

            transaction

        )



    output = []



    # -----------------------------------------------------
    # Decode SPI header
    # -----------------------------------------------------


    header = decode_spi_header(

        transaction

    )



    output.append(

        format_spi_header(header)

    )



    output.append(

        "\n==============================\n"

    )



    payload = header["payload"]



    # -----------------------------------------------------
    # Find register
    # -----------------------------------------------------


    register_name = get_register(

        header["register_offset"]

    )



    output.append(

        f"Detected Register : {register_name}"

    )



    output.append("")



    # -----------------------------------------------------
    # FIFO command path
    # -----------------------------------------------------


    if register_name in [

        "TPM_DATA_FIFO",

        "TPM_X_DATA_FIFO"

    ]:



        if is_fifo_stream(payload):


            output.append(

                "FIFO contains TPM command"

            )


            output.append(

                "\n==============================\n"

            )



            result = decode_tpm_command(

                payload

            )



            output.append(

                result["decoded"]

            )



        else:


            output.append(

                decode_register(

                    register_name,

                    header["operation"],

                    payload

                )

            )



    # -----------------------------------------------------
    # Normal register path
    # -----------------------------------------------------


    else:


        output.append(

            decode_register(

                register_name,

                header["operation"],

                payload

            )

        )



    return "\n".join(output)



# =========================================================
# SELF TEST
# =========================================================


if __name__ == "__main__":



    # TPM_STS example


    packet = (

        "80 D4 00 18 C0"

    )



    print(

        decode_mosi(packet)

    )



    print(

        "\n\n---------------------------\n\n"

    )



    # TPM Startup command in FIFO


    fifo_packet = (

        "80 D4 00 24 "

        "80 01 "

        "00 00 00 0C "

        "00 00 01 44 "

        "00 00"

    )



    print(

        decode_mosi(

            fifo_packet

        )

    )