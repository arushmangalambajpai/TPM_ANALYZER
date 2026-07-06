"""
decode_full.py

Complete TPM SPI Transaction Decoder.

This file combines MOSI and MISO.

Purpose:

SPI transaction

    MOSI + MISO

        ↓

SPI Header Decode

        ↓

Register Detection

        ↓

Choose correct data source

        ↓

Register / FIFO / TPM Decode


Rules:

WRITE:
    Payload comes from MOSI

READ:
    Payload comes from MISO


This file does NOT:
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


from tpm_analyzer.tpm.response import (
    decode_tpm_response
)


from tpm_analyzer.utils.byte_utils import (
    hex_to_bytes,
    bytes_to_hex
)



# =========================================================
# FULL TRANSACTION DECODER
# =========================================================


def decode_full(
        mosi,
        miso,
        previous_command_code=None
):

    """
    Decode complete TPM SPI transaction.

    Input:

        MOSI

        MISO

    Output:

        {
            text,
            command_code
        }
    """


    # -----------------------------------------------------
    # Input conversion
    # -----------------------------------------------------


    if isinstance(mosi, str):

        mosi = hex_to_bytes(
            mosi
        )


    if isinstance(miso, str):

        miso = hex_to_bytes(
            miso
        )



    output = []



    # =====================================================
    # RAW TRANSACTION
    # =====================================================


    output.append(
        "================================"
    )


    output.append(
        "RAW SPI TRANSACTION"
    )


    output.append(
        "================================"
    )


    output.append(
        ""
    )


    output.append(
        "MOSI:"
    )


    output.append(
        bytes_to_hex(mosi)
    )


    output.append(
        ""
    )


    output.append(
        "MISO:"
    )


    output.append(
        bytes_to_hex(miso)
    )


    output.append(
        ""
    )



    # =====================================================
    # HEADER
    # =====================================================


    header = decode_spi_header(
        mosi
    )


    output.append(
        "================================"
    )


    output.append(
        "SPI HEADER (FROM MOSI)"
    )


    output.append(
        "================================"
    )


    output.append(
        ""
    )


    output.append(
        format_spi_header(header)
    )


    output.append(
        ""
    )



    # =====================================================
    # REGISTER
    # =====================================================


    register = get_register(
        header["register_offset"]
    )


    output.append(
        "================================"
    )


    output.append(
        "REGISTER INFORMATION"
    )


    output.append(
        "================================"
    )


    output.append(
        ""
    )


    output.append(
        f"Register : {register}"
    )


    output.append(
        ""
    )



    # =====================================================
    # DATA SOURCE
    # =====================================================


    if header["operation"] == "WRITE":


        payload = header["payload"]


        source = "MOSI"



    else:


        payload = miso[4:]


        source = "MISO"



    output.append(
        f"Data Source : {source}"
    )


    output.append(
        ""
    )


    output.append(
        "Payload:"
    )


    output.append(
        bytes_to_hex(payload)
    )


    output.append(
        ""
    )



    # =====================================================
    # FIFO
    # =====================================================


    if register in [

        "TPM_DATA_FIFO",

        "TPM_X_DATA_FIFO"

    ]:



        output.append(
            "================================"
        )


        output.append(
            "FIFO DECODE"
        )


        output.append(
            "================================"
        )


        output.append("")



        if is_fifo_stream(payload):


            if header["operation"] == "WRITE":


                output.append(
                    "Detected : TPM COMMAND"
                )


                output.append("")


                result = decode_tpm_command(
                    payload
                )


                output.append(
                    result["decoded"]
                )


                return {


                    "text":
                        "\n".join(output),


                    "command_code":
                        result["command_code"]

                }



            else:


                output.append(
                    "Detected : TPM RESPONSE"
                )


                output.append("")


                if previous_command_code is None:


                    output.append(
                        "WARNING:"
                    )


                    output.append(
                        "Previous command code missing."
                    )



                else:


                    result = decode_tpm_response(

                        payload,

                        previous_command_code

                    )


                    output.append(
                        result["decoded"]
                    )



        else:


            output.append(

                decode_register(

                    register,

                    header["operation"],

                    payload

                )

            )



    # =====================================================
    # REGISTER DECODE
    # =====================================================


    else:


        output.append(
            "================================"
        )


        output.append(
            "REGISTER DECODE"
        )


        output.append(
            "================================"
        )


        output.append("")


        output.append(

            decode_register(

                register,

                header["operation"],

                payload

            )

        )



    return {


        "text":

            "\n".join(output),


        "command_code":

            previous_command_code

    }




# =========================================================
# SELF TEST
# =========================================================


if __name__ == "__main__":


    tests = [


        (
            "TPM_STS READ",

            "00 D4 00 18 00",

            "00 00 00 00 D4"

        ),



        (
            "TPM_ACCESS READ",

            "00 D4 00 00 00",

            "00 00 00 00 A2"

        ),



        (
            "TPM_STS WRITE commandReady",

            "80 D4 00 18 40",

            "00 00 00 00 00"

        )

    ]



    for name,mosi,miso in tests:


        print(

            "\n\n########",

            name,

            "########\n"

        )


        result = decode_full(

            mosi,

            miso

        )


        print(

            result["text"]

        )