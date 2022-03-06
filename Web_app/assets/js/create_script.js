function new_data(form, data_type) {
    let form_data = new FormData(form);
    let token = getCookie('authorization');
    if (data_type === 'employee'){
        form_data.set('password', hashPass(form.password.value));
        if (form_data.get('activated') !== null) {
            form_data.set('activated', '1');
        } else {
            form_data.set('activated', '0');
        }
    }
    fetch(`${api_url}/create/${data_type}`, {method: "POST", body: form_data, headers: {'authorization': token}})
        .then(resp => {
            if (resp.status === 201) {
                setCookie('message', 'success:Transakcja zakończona pomyślnie)', 5);
                window.location.reload();
            } else {
                setCookie('message', 'error:Coś poszło nie tak (skontaktuj się z administratorem)', 5);
                window.location.reload();
            }
        })
        .catch(function(error) {
            console.log(error);
        });
}