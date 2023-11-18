function update_data(form, data_type) {
    console.log(form)
    let form_data = new FormData(form);
    console.log(form_data.get('id_entity'));
    let token = getCookie('authorization');
    if (data_type === 'employee'){
        console.log(form_data.get('department'));
        if (form_data.get('activated') !== null) {
            form_data.set('activated', '1');
        } else {
            form_data.set('activated', '0');
        }
        if (form_data.get('admin_permissions') !== null) {
            form_data.set('admin_permissions', '1');
        } else {
            form_data.set('admin_permissions', '0');
        }
        console.log(form_data.get('activated'), form_data.get('admin_permissions'))
    }
    fetch(`${api_url}/update/${data_type}`, {method: "POST", body: form_data, headers: {'authorization': token}})
        .then(resp => {
            if (resp.status === 201) {
                setCookie('message', 'success:Transakcja zakończona pomyślnie)', 5);
                // window.location.reload();
            } else {
                setCookie('message', 'error:Coś poszło nie tak (skontaktuj się z administratorem)', 5);
                // window.location.reload();
            }
        })
        .catch(function(error) {
            console.log(error);
        });
}