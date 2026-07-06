"""
response.py

TPM Response Decoder Layer.

This file provides TPM Analyzer's
internal response decoding interface.

It uses:

    tpmstream_wrapper.py

but never directly imports tpmstream.


Important:

TPM responses DO NOT contain command codes.

The previous TPM commandCode is required
to decode response parameters correctly.


This file does NOT:
- Decode SPI
- Decode registers
- Decode FIFO
"""


from tpm_analyzer.tpm.tpmstream_wrapper import (
    decode_response
)


from tpm_analyzer.utils.byte_utils import (
    read_uint32
)



# =========================================================
# RESPONSE CODE EXTRACTION
# =========================================================


def get_response_code(response_bytes):

    """
    Extract TPM_RC from response.


    TPM response format:


    bytes 0-1:

        tag


    bytes 2-5:

        size


    bytes 6-9:

        responseCode
    """


    if len(response_bytes) < 10:


        return None



    return read_uint32(

        response_bytes,

        6

    )



# =========================================================
# TPM RESPONSE DECODER
# =========================================================


def decode_tpm_response(
        response_bytes,
        command_code
):

    """
    Decode complete TPM response.


    Input:

        response_bytes:

            TPM FIFO response


        command_code:

            TPM_CC of previous command


    Output:


        {
            response_code,

            decoded
        }

    """



    response_code = get_response_code(

        response_bytes

    )



    decoded = decode_response(

        response_bytes,

        command_code

    )



    return {


        "response_code":

            response_code,



        "decoded":

            decoded


    }



# =========================================================
# SELF TEST
# =========================================================


if __name__ == "__main__":



    # Example:
    #
    # Generic successful response


    response = [


        0x80,0x01,


        0x00,0x00,0x00,0x0A,


        0x00,0x00,0x00,0x00


    ]



    # TPM2_Startup

    command_code = 0x00000144



    result = decode_tpm_response(

        response,

        command_code

    )



    print(

        "RESPONSE CODE:",

        hex(result["response_code"])

    )



    print()



    print(

        result["decoded"]

    )