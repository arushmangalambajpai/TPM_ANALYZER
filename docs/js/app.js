/*
app.js

TPM SPI LOG DECODER

Browser frontend.
*/


let pyodide = null;


// =====================================================
// START PYTHON
// =====================================================


async function startPython()
{


    printOutput(
        "Loading Python Runtime..."
    );



    pyodide =
        await loadPyodide();




    printOutput(
        "Loading TPM Analyzer..."
    );



    let zipResponse =
        await fetch(

            "python/tpm_analyzer.zip"

        );



    let zipData =
        await zipResponse.arrayBuffer();




    pyodide.FS.writeFile(

        "tpm_analyzer.zip",

        new Uint8Array(

            zipData

        )

    );





    await pyodide.runPythonAsync(`


import zipfile
import sys


zipfile.ZipFile(

    "tpm_analyzer.zip"

).extractall(

    "."

)


sys.path.insert(

    0,

    "."

)


    `);





    let runner =

        await fetch(

            "python/web_runner.py"

        );




    let code =

        await runner.text();




    await pyodide.runPythonAsync(

        code

    );




    document.getElementById(

        "status"

    ).innerText =

        "Python Ready";




    printOutput(

        "TPM SPI Analyzer Ready"

    );


}




// =====================================================
// OPTION A : MOSI
// =====================================================


async function runMosi()
{


    let data =

        document.getElementById(

            "mosi"

        ).value;




    let result =

        await pyodide.runPythonAsync(`


web_mosi(

r"""${data}"""

)


        `);




    printOutput(

        result

    );


}





// =====================================================
// OPTION B : COMPLETE TRANSACTION
// =====================================================


async function runFull()
{


    let mosi =

        document.getElementById(

            "full_mosi"

        ).value;




    let miso =

        document.getElementById(

            "full_miso"

        ).value;




    let result =

        await pyodide.runPythonAsync(`


web_full(

r"""${mosi}""",

r"""${miso}"""

)


        `);




    printOutput(

        result

    );


}






// =====================================================
// LOAD CSV
// =====================================================


async function loadCSV()
{


    let file =

        document.getElementById(

            "csv"

        ).files[0];



    if(

        !file

    )
    {

        alert(

            "Select CSV first"

        );


        return;

    }



    let text =

        await file.text();




    let result =

        await pyodide.runPythonAsync(`


web_load_csv(

r"""${text}"""

)


        `);




    printOutput(

        result

    );


}






// =====================================================
// CSV OPTION 1
// =====================================================


async function runTransactions()
{


    let result =

        await pyodide.runPythonAsync(

            "web_transactions()"

        );




    printOutput(

        result

    );


}






// =====================================================
// CSV OPTION 2
// =====================================================


async function runDecodeSheet()
{


    let result =

        await pyodide.runPythonAsync(

            "web_decode_sheet()"

        );




    printOutput(

        result

    );


}






// =====================================================
// CSV OPTION 4
// =====================================================


async function runCommands()
{


    let result =

        await pyodide.runPythonAsync(

            "web_commands()"

        );




    printOutput(

        result

    );


}






// =====================================================
// CSV OPTION 5
// =====================================================


async function runPCR()
{


    let result =

        await pyodide.runPythonAsync(

            "web_pcr()"

        );




    printOutput(

        result

    );


}





// =====================================================
// UI
// =====================================================


function showPanel(id)
{


    document.querySelectorAll(

        ".panel"

    ).forEach(


        element =>

            element.style.display="none"

    );




    document.getElementById(

        id

    ).style.display="block";


}





function printOutput(text)
{


    let ansi =
        new AnsiUp();



    let html =
        ansi.ansi_to_html(

            text

        );



    document.getElementById(

        "output"

    ).innerHTML = html;


}

// =====================================================
// TPM FIFO COMMAND DECODE
// =====================================================



async function runSingleTransaction()
{


let index =
prompt(
"Enter Transaction Index"
);



if(
!index
)
{

return;

}



let result =
await pyodide.runPythonAsync(`

web_single_transaction(

"${index}"

)

`);



printOutput(

result

);


}

// =====================================================
// DOWNLOAD GENERATED FILES
// =====================================================


function downloadFile(
    path,
    filename
)
{


    try
    {


        let data =
            pyodide.FS.readFile(

                path,

                {

                    encoding:"utf8"

                }

            );



        let blob =
            new Blob(

                [data],

                {

                    type:"text/plain"

                }

            );



        let link =
            document.createElement(

                "a"

            );



        link.href =
            URL.createObjectURL(

                blob

            );



        link.download =
            filename;



        link.click();



        URL.revokeObjectURL(

            link.href

        );


    }


    catch(error)
    {


        alert(

            "File not generated yet"

        );


    }


}

startPython();