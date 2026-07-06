"""
tpmstream_wrapper.py

Wrapper around external tpmstream library.

This is the ONLY file that imports
and communicates with tpmstream.

Purpose:

Raw TPM bytes

        ↓

tpmstream

        ↓

Human readable TPM structures


This file does NOT:
- Decode SPI
- Decode registers
- Decode FIFO
"""


# =========================================================
# IMPORT TPMSTREAM
# =========================================================


try:

    import tpmstream


except ImportError:


    tpmstream = None



# =========================================================
# TPM COMMAND DECODER
# =========================================================


def decode_command(command_bytes):

    """
    Decode TPM command bytes.

    Input:

        Complete TPM command:

        80 02
        00 00 00 35
        00 00 01 82
        ...


    Output:

        Text output from tpmstream
    """


    if tpmstream is None:

        return (
            "ERROR:\n"
            "tpmstream library not installed."
        )


    try:


        # Placeholder wrapper.
        #
        # Actual tpmstream API connection
        # happens here.


        decoded = tpmstream.decode(
            command_bytes
        )


        return str(decoded)



    except Exception as error:


        return (

            "TPM Command Decode Failed\n\n"

            f"Error:\n{error}"

        )



# =========================================================
# TPM RESPONSE DECODER
# =========================================================


def decode_response(
        response_bytes,
        command_code
):

    """
    Decode TPM response.

    TPM response requires previous command.

    Input:

        response bytes

        command_code


    Example:

        response:
            80 01....

        command:
            TPM_CC_PCR_Extend
    """


    if tpmstream is None:


        return (
            "ERROR:\n"
            "tpmstream library not installed."
        )



    try:


        decoded = tpmstream.decode(
            response_bytes,
            command_code
        )


        return str(decoded)



    except Exception as error:


        return (

            "TPM Response Decode Failed\n\n"

            f"Command Code:\n{command_code}\n\n"

            f"Error:\n{error}"

        )



# =========================================================
# SELF TEST
# =========================================================


if __name__ == "__main__":


    sample = [

        0x80,0x01,

        0x00,0x00,0x00,0x0A,

        0x00,0x00,0x01,0x44

    ]



    print(
        decode_command(
            sample
        )
    )