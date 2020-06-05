$(document).ready(function () {
    // HACK: This should be window.Terminal once upgraded to 4.0.1
    var term = new Terminal({rows: 30, cols: 180});
    term.open(document.getElementById('terminal'));
    var ipaddr = null;
    var socket = io('/');
    var termEnv = '\r\n[' + hostname + ']$ ';

    function InitTerminal() {
        term.clear();
    }

    function runFakeTerminal() {
        if (term._initialized) {
            return;
        }
        term._initialized = true;

        term.prompt = () => {
            term.write('\r\n[\\u@\\h \\W]\\$ ');
        };
        term.writeln('Welcome to Pitta Cmdb');
        term.writeln('This is a local terminal emulation, without a real terminal in the back-end.');
        term.writeln('Type some keys and commands to play around.');
        term.writeln('');
        prompt(term);
        var command = '';

        term.onKey(e => {
            command += e.key;
            const printable = !e.domEvent.altKey && !e.domEvent.altGraphKey && !e.domEvent.ctrlKey && !e.domEvent.metaKey;
            if (e.domEvent.keyCode === 13) {
                exec_command(command);
                command = '';
            } else if (e.domEvent.keyCode === 8) {
                // Do not delete the prompt
                if (term._core.buffer.x > termEnv.length+2) {
                    term.write('\b \b');
                    command = command.substring(0, command.length - 2)
                }
            } else if (printable) {
                term.write(e.key);
            }
        });

        socket.on('new command', function (data) {
            if (data.code == 0) {
                term.write("\r\n" + data.result);
                prompt(term);
            }
            if (data.code == 2) {
                term._initialized = false;
            }
        });
    }

    function prompt(term) {
        term.write(termEnv);
    }

    function exec_command(command) {
        if (command == 'clear\r') {
            term.clear();
            prompt(term);
        } else if (command == 'exit\r') {
            term._initialized = false;
            //term.clear();
        } else {
            socket.emit('new command', {'ip': private_ip, 'command': command})
        }
    }

    $(document).on('click', '#connect', function (e) {
        var ip = $('#ip').val();
        var username = $('#username').val();
        var password = $('#password').val();
        $.ajax({
            url: connect_url,
            method: 'post',
            data: JSON.stringify({'ip': ip, 'username': username, 'password': password}),
            headers: {'Content-Type': 'application/json;charset=utf8'},
            success: function (data) {
                ipaddr = ip;
                runFakeTerminal();
                $('#terminal').show();
                $('#ssh').modal('hide');
                toastr.success('连接成功');
            },
            error: function (e) {
                toastr.error(e.responseJSON.msg);
            }
        })
    });

    $(document).on('click', '#close', function (e) {
        $.ajax({
            url: close_connect_url,
            method: 'post',
            data: JSON.stringify({'ip': ipaddr}),
            headers: {'Content-Type': 'application/json;charset=utf8'},
            success: function (data) {
                InitTerminal();
                $('#terminal').hide();
                toastr.success(data.msg);
            },
            error: function (e) {
                toastr.error(e.responseJSON.msg);
            }
        })
    });
});