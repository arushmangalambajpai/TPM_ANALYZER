"""
register_map.py

TPM FIFO Interface Register Map.

This file only maps register offsets
to register names.

It does NOT:
- Decode register contents
- Decode bit fields
- Decode TPM commands


Register addressing:

SPI gives:

    D4 L R R

Example:

    D4 20 18

SPI decoder extracts:

    Locality:
        2

    Offset:
        018h


This file only receives:

    018h
"""


# =========================================================
# TPM REGISTER MAP
# =========================================================


TPM_REGISTER_MAP = [

    {
        "name": "TPM_ACCESS",
        "start": 0x000,
        "end":   0x000
    },


    {
        "name": "TPM_INT_ENABLE",
        "start": 0x008,
        "end":   0x00B
    },


    {
        "name": "TPM_INT_VECTOR",
        "start": 0x00C,
        "end":   0x00C
    },


    {
        "name": "TPM_INT_STATUS",
        "start": 0x010,
        "end":   0x013
    },


    {
        "name": "TPM_INTF_CAPABILITY",
        "start": 0x014,
        "end":   0x017
    },


    {
        "name": "TPM_STS",
        "start": 0x018,
        "end":   0x01B
    },


    {
        "name": "TPM_DATA_FIFO",
        "start": 0x024,
        "end":   0x027
    },


    {
        "name": "TPM_INTERFACE_ID",
        "start": 0x030,
        "end":   0x033
    },


    {
        "name": "TPM_DATA_CSUM_ENABLE",
        "start": 0x034,
        "end":   0x038
    },


    {
        "name": "TPM_DATA_CSUM",
        "start": 0x038,
        "end":   0x03B
    },


    {
        "name": "TPM_X_DATA_FIFO",
        "start": 0x080,
        "end":   0x083
    },


    {
        "name": "TPM_DID_VID",
        "start": 0xF00,
        "end":   0xF03
    },


    {
        "name": "TPM_RID",
        "start": 0xF04,
        "end":   0xF04
    },


    {
        "name": "VENDOR_SPECIFIC",
        "start": 0xF90,
        "end":   0xFFF
    }

]


# =========================================================
# REGISTER LOOKUP
# =========================================================


def get_register(offset):

    """
    Find TPM register from offset.


    Input:

        integer:

            0x018


        OR

        string:

            "0018"


    Output:

        Register name
    """


    if isinstance(offset, str):

        offset = int(
            offset,
            16
        )



    for register in TPM_REGISTER_MAP:


        if (
            register["start"]
            <=
            offset
            <=
            register["end"]
        ):

            return register["name"]



    return "RESERVED"



# =========================================================
# SELF TEST
# =========================================================


if __name__ == "__main__":


    tests = [

        "0000",

        "0018",

        "0019",

        "0024",

        "0F00",

        "0F04",

        "0F95",

        "0050"

    ]



    for test in tests:


        print(
            test,
            "->",
            get_register(test)
        )