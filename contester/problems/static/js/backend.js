let editor2 = CodeMirror.fromTextArea(document.getElementById("editor"), {
    value: "asdad\n",
    lineNumbers: true,
    mode: "text/x-c++src",
    autoCloseBrackets: true
}).doc;

//;

console.log(editor2);

function submitClick() {
    let code = editor2.getValue("\n");
    if (code === '') {
        alert("You are trying to sent an empty code.");
        return;
    }

    let xhr = new XMLHttpRequest();
    xhr.open("POST", "http://127.0.0.1:5000/compiler/check_code");

    let data = JSON.stringify({
        "problem_id": 1,
        "code": code
    });

    xhr.send(data);
}


