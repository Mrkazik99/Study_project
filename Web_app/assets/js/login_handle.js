function checkToken() {
    let token = getCookie('authorization');
    if (token !== "") {
        fetch(`${api_url}/check_token`, {method: "GET", mode: "cors", headers: {'authorization': token}})
            .then(resp => {
                if (resp.status !== 200) {
                    setCookie('message', 'Ta treść jest dostępna po zalogowaniu', 5);
                    console.log('error token');
                    window.location.href="/";
                }
            })
            .catch(function(error) {
                console.log(error);
                setCookie('authorization', '');
                setCookie('message', 'Internal server error, contact your administrator', 5);
                window.location.href="/";
            });
    } else {
        setCookie('authorization', '');
        setCookie('message', 'You have no valid token active', 5);
        window.location.href="/";
    }
}

function hashPass(passphrase) {
    let passObj = passphrase
    let hashObj = new jsSHA("SHA-512", "TEXT", {numRounds: 1});
    hashObj.update(passObj);
    return hashObj.getHash("HEX");
}

function submit_login(form) {
    if (form.password === '' || form.username.value === '') {
        setCookie('message', 'Nieprawidłowe dane logownaia', 5);
        window.location.href='/';
    }
    let form_data = new FormData(form);
    form_data.set('password', hashPass(form.password));
    let payload = form_data
    console.log(payload)
    fetch(`${api_url}/login`, {method: "POST", body: payload})
        .then(resp => {
            console.log(resp);
            if (resp.status === 200) {
                return resp.json()
            } else {
                setCookie('message', 'Nieprawidłowe dane logownaia', 5);
                window.location.href='/';
            }
        })
        .then(data => {
            setCookie('authorization', `${data['token']}`, token_time);
            window.location.href='/dashboard.html';
        })
        .catch(function(error) {
            console.log(error);
        });
}

function setCookie(cname, cvalue, exminutes) {
    const d = new Date();
    d.setTime(d.getTime() + (exminutes*60*1000));
    let expires = "expires="+ d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

function getCookie(cname) {
    let name = cname + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(';');
    for(let i = 0; i <ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) === ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) === 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

function logout(token) {
    fetch(`${api_url}/logout`, {method: "GET", mode: "cors", headers: {'authorization': token}})
        .then(resp => {
            if (resp.status === 200) {
                setCookie('message', 'Wylogowano pomyślnie', 5);
            }
        })
        .catch(function(error) {
            console.log(error);
        });
}