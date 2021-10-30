let editor2 = CodeMirror.fromTextArea(document.getElementById("editor"), {
    value: "asdad\n",
    lineNumbers: true,
    mode: "text/x-c++src",
    autoCloseBrackets: true
}).doc;

function submitClick() {
    let code = editor2.getValue("\n");
    if (code === '') {
        alert("You are trying to sent an empty code.");
        return;
    }

    let xhr = new XMLHttpRequest();
    xhr.open("POST", "http://" + PAYLOAD.host + ":5000/compiler/check_code");

    let data = JSON.stringify({
        "problem_id": PAYLOAD.id,
        "code": code
    });


    xhr.send(data);

    xhr.onload = function() {
        let result = JSON.parse(xhr.responseText);
        if (result['accepted']) {
            alert("Ну чё, заебись, аккептед.");
        } else {
            alert("Лох))0)");
        }
    }

}


