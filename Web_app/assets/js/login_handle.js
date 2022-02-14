function checkToken() {
    let token = getCookie('authorization');
    if (token !== "") {
        fetch(`${api_url}/check_token`, {method: "GET", mode: "cors", headers: {'authorization': token}})
            .then(resp => {
                console.log(resp);
                if (resp.status !== 200) {
                    window.location.href="/";
                }
            })
            .catch(function(error) {
                console.log(error);
            });
    }
}

function hashPass() {
    let pwdObj = document.getElementById('password');
    let hashObj = new jsSHA("SHA-512", "TEXT", {numRounds: 1});
    hashObj.update(pwdObj.value);
    pwdObj.value = hashObj.getHash("HEX");
}

function submit_login(form) {
    let payload = {};
    fetch(``, {method: "POST", mode: "cors"})
        .then(resp => {
            console.log(resp);
            if (resp.status === 200) {
                return resp.json()
            } else {

            }
        })
        .then(data => {
            setCookie('authorization', `${data['token']}`, 40);
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