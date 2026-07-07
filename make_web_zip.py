import os
import zipfile


OUTPUT = "docs/python/tpm_analyzer.zip"


PACKAGES = [

    "tpm_analyzer",

    "tpmstream",

    "colorama"

]


if os.path.exists(
    OUTPUT
):

    os.remove(
        OUTPUT
    )


with zipfile.ZipFile(
    OUTPUT,
    "w",
    zipfile.ZIP_DEFLATED
) as z:


    for package in PACKAGES:


        for root, dirs, files in os.walk(
            package
        ):


            if "__pycache__" in root:

                continue


            for file in files:


                full = os.path.join(
                    root,
                    file
                )


                archive = full.replace(
                    "\\",
                    "/"
                )


                z.write(
                    full,
                    archive
                )


print(
    "Created web package"
)