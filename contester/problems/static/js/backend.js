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
    xhr.open("POST", "http://" + PAYLOAD.host + "/compiler/check_code");

    let data = JSON.stringify({
        "problem_id": PAYLOAD.problem_id,
        "code": code
    });

    xhr.send(data);

    xhr.onload = function() {
        let result = JSON.parse(xhr.responseText);

        save_attempt(PAYLOAD.problem_id, result, code);

        if (result['accepted']) {
            alert("Ну чё, заебись, аккептед.");
        } else {
            alert("Лох))0)");
        }
    }

}

function save_attempt(problem_id, result, code) {
    let xhr = new XMLHttpRequest();
    xhr.open("POST", "http://" + PAYLOAD.host + "/problems/save_attempt");

    let today = new Date();
    let current_date = today.getFullYear() + '-' + today.getMonth() + '-' + today.getDate();
    let current_time = today.getHours() + ':' + today.getMinutes() + ':' + today.getSeconds();

    let data = JSON.stringify({
        'problem_id': PAYLOAD.problem_id,
        'status': result['status'],
        'error': result['error'],
        'log': result['log'],
        'accepted': result['accepted'],
        'failed_case': result['sample_index'],
        'code': code,
        'submitted_date': current_date + ' ' + current_time
    });

    xhr.send(data);
}