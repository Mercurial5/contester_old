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

    let current_date = new Date();
    add_attempt(get_date_from_Date(current_date));

    let xhr = new XMLHttpRequest();
    xhr.open("POST", "http://" + PAYLOAD.host + "/compiler/check_code");

    let data = JSON.stringify({
        "problem_id": PAYLOAD.problem_id,
        "code": code
    });

    xhr.send(data);

    xhr.onload = function() {
        let result = JSON.parse(xhr.responseText);

        let attempt_id = save_attempt(PAYLOAD.problem_id, result, current_date / 1000, code);
        update_attempt(result, get_date_from_Date(current_date), attempt_id);
    }

}

function save_attempt(problem_id, result, current_timestamp, code) {
    let xhr = new XMLHttpRequest();
    xhr.open("POST", "http://" + PAYLOAD.host + "/problems/save_attempt");

    let data = JSON.stringify({
        'problem_id': PAYLOAD.problem_id,
        'status': result['status'],
        'error': result['error'],
        'log': result['log'],
        'accepted': result['accepted'],
        'failed_case': result['sample_index'],
        'code': code,
        'submitted_time': current_timestamp
    });

    xhr.send(data);
    let attempt_id;
    xhr.onload = function () {
        let result = JSON.parse(xhr.responseText);
        attempt_id = result['attempt_id'];
    }
    return attempt_id;
}

function add_attempt(current_date) {
    let string_attempt = '<div class="attempt-info border">\n' +
        '                    <a class="two-inline-blocks pb-3">\n' +
        '                        <div class="pl-4 pt-3">\n' +
        '                            <div class="attempt-result">\n' +
        '                                \n' +
        '                                    Checking...\n' +
        '                                \n' +
        '                            </div>\n' +
        '                            <p class="failed-task pt-2">\n' +
        '                                \n' +
        '                            </p>\n' +
        '                        </div>\n' +
        '                        <div class="attempt-date pt-3 pr-4">\n' +
        '                            ' + current_date + '\n' +
        '                        </div>\n' +
        '                    </a>\n' +
        '                </div>';

    let attempts_block = document.getElementById('attempts-wrapper');
    let attempt = document.createElement('div');
    attempt.innerHTML = string_attempt.trim();
    attempts_block.insertBefore(attempt, attempts_block.firstChild);

    for (let i = 0; i <= attempts_block.children.length - 10; i++) {
        attempts_block.removeChild(attempts_block.lastChild);
    }
}

function update_attempt(result, current_date, attempt_id) {
    let url_to_attempt = "http://" + PAYLOAD.host + "/problems/show_attempt/" + attempt_id;
    let attempts_block = document.getElementById('attempts-wrapper');
    let last_attempt = attempts_block.firstChild;

    let first_message = undefined;
    let failed_case = '';
    let color_name = '';
    if (result['status'] === false) {
        first_message = result['error'];
        color_name = 'error-attempt';
    } else {
        if (result['accepted'] === true) {
            first_message = 'Accepted';
            color_name = 'accepted-attempt'
        } else {
            first_message = 'Wrong Answer';
            failed_case = 'Failed on case ' + result['sample_index'];
            color_name = 'wrong-attempt';
        }
    }

    let string_attempt = '<div class="attempt-info border ' + color_name + '">\n' +
        '                    <a class="two-inline-blocks pb-3" href="' + url_to_attempt + '">\n' +
        '                        <div class="pl-4 pt-3">\n' +
        '                            <div class="attempt-result">\n' +
        '                                \n' +
        '                                    ' + first_message + '\n' +
        '                                \n' +
        '                            </div>\n' +
        '                            <p class="failed-task pt-2">\n' +
        '                                ' + failed_case + '\n' +
        '                            </p>\n' +
        '                        </div>\n' +
        '                        <div class="attempt-date pt-3 pr-4">\n' +
        '                            ' + current_date + '\n' +
        '                        </div>\n' +
        '                    </a>\n' +
        '                </div>';

    let new_attempt = document.createElement('div');
    new_attempt.innerHTML = string_attempt;
    last_attempt.replaceWith(new_attempt);
}

function get_date_from_Date(current_date) {
    let current_time = current_date.getFullYear() + '-' + addZeroBefore(current_date.getMonth() + 1) + '-' + addZeroBefore(current_date.getDate());
    current_date = current_time + ' ' + addZeroBefore(current_date.getHours()) + ':' + addZeroBefore(current_date.getMinutes()) + ':' + addZeroBefore(current_date.getMinutes());
    return current_date;
}

function addZeroBefore(n) {
  return (n < 10 ? '0' : '') + n;
}