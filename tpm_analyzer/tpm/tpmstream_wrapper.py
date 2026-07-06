"""
tpmstream_wrapper.py

Wrapper around external tpmstream library.

This is the ONLY file that directly imports
and communicates with tpmstream.

Purpose:

TPM command / response bytes

        ↓

tpmstream

        ↓

Human readable TPM tree


This file does NOT:
- Decode SPI
- Decode registers
- Decode FIFO
"""


# =========================================================
# IMPORT TPMSTREAM
# =========================================================


try:

    from tpmstream.io.binary import Binary

    from tpmstream.io.pretty import Pretty

    from tpmstream.spec.commands import (
        Command,
        Response
    )


except ImportError:


    Binary = None

    Pretty = None

    Command = None

    Response = None



# =========================================================
# HELPER
# =========================================================


def list_to_bytes(data):

    """
    Convert list:

        [0x80,0x01]

    into:

        b'\\x80\\x01'
    """


    return bytes(data)



def pretty_output(events):

    """
    Convert tpmstream events
    into readable string.
    """


    output = []


    pretty = Pretty.unmarshal(
        events
    )


    for line in pretty:

        output.append(
            str(line)
        )


    return "\n".join(output)



# =========================================================
# TPM COMMAND DECODER
# =========================================================


def decode_command(command_bytes):

    """
    Decode TPM command.


    Input:

        list of bytes


    Example:

        [
        0x80,0x01,
        0x00,0x00,0x00,0x0C,
        0x00,0x00,0x01,0x44
        ]


    Output:

        Pretty TPM structure
    """


    if Binary is None:


        return (
            "ERROR:\n"
            "tpmstream not installed"
        )



    try:


        buffer = list_to_bytes(
            command_bytes
        )


        events = Binary.marshal(

            tpm_type = Command,

            buffer = buffer,

            abort_on_error = False

        )



        return pretty_output(
            events
        )



    except Exception as error:


        return (

            "TPM Command Decode Failed\n\n"

            f"{error}"

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


    Response needs:

        - response bytes

        - previous TPM command code
    """


    if Binary is None:


        return (
            "ERROR:\n"
            "tpmstream not installed"
        )



    try:


        buffer = list_to_bytes(
            response_bytes
        )



        events = Binary.marshal(

            tpm_type = Response,

            buffer = buffer,

            command_code = command_code,

            abort_on_error = False

        )



        return pretty_output(
            events
        )



    except Exception as error:


        return (

            "TPM Response Decode Failed\n\n"

            f"Command Code : {command_code}\n\n"

            f"{error}"

        )



# =========================================================
# SELF TEST
# =========================================================


if __name__ == "__main__":


    startup_command = [

        0x80,0x01,

        0x00,0x00,0x00,0x0C,

        0x00,0x00,0x01,0x44,

        0x00,0x00

    ]



    print(

        decode_command(

            startup_command

        )

    )