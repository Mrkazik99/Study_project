function update_field (datalist, text_input, select) {
    let dataset = $(`#${datalist}`).children();
    for (let i = 0; i < dataset.length; i++) {
        if (dataset[i].getAttribute('value') === select.value) {
            $(`#${text_input}`).val(dataset[i].innerHTML);
            break;
        }
    }
}

function parseJwt (token) {
    let base64Url = token.split('.')[1];
    let base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    let jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {
        return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
    }).join(''));

    return JSON.parse(jsonPayload);
}

function getEmployees(elem) {
    let token = getCookie('authorization');
    fetch('http://127.0.0.1:20001/get/employees', {method: "GET", mode: "cors", headers: {'authorization': token}})
        .then((resp) => resp.json())
        .then(function(data) {
            let table = '';
            data.forEach(element => {
                if (element['id'] === parseInt(elem.attr('data-value'))) {
                    table += `<option value="${element['id']}" selected>${element['name']} - ${element['department']}</option>`;
                } else {
                    table += `<option value="${element['id']}">${element['name']} - ${element['department']}</option>`;
                }
            })
            elem.html(table);
        });
}

function getDepartments(elem) {
    let token = getCookie('authorization');
    fetch('http://127.0.0.1:20001/get/departments', {method: "GET", mode: "cors", headers: {'authorization': token}})
        .then((resp) => resp.json())
        .then(function(data) {
            let table = '';
            data.forEach(element => {
                if (element['id'] === parseInt(elem.attr('data-value'))) {
                    table += `<option value="${element['id']}" selected>${element['name']} - ${element['department']}</option>`;
                } else {
                    table += `<option value="${element['id']}">${element['name']} - ${element['department']}</option>`;
                }
            })
            elem.html(table);
        });
}

function tableParserReq(data) {
    let content = `<table class="table align-middle"><thead><tr><th scope="col">Id</th><th scope="col">Data przyjęcia</th><th scope="col">Data aktualizacji</th><th scope="col">Klient</th><th scope="col">Przedmiot</th><th scope="col">Stan</th><th scope="col">Akcje</th></tr></thead><tbody>`
    data.forEach(element => {
        // if (new Date() - element['date0'] >= 2592000000 || new Date() - element['date1'] >= 2592000000){
        if (new Date() - new Date(element['date0']) >= 86400000 * 7 || new Date() - new Date(element['date1']) >= 86400000 * 7){
            content += `<tr class="table-danger data_row`;
            if (default_hidden.indexOf(element['status']) !== -1 && !$('#request_gone').val()) {
                content += ' hidden';
            }
            content += `" data-status="${element['status']}"><td>${element['id']}</td><td>${element['date0']}</td><td>${element['date1']}</td><td>${element['customer']}</td><td>${element['item']}</td><td>${statuses[element['status']]}</td><td><a type="button" class="btn btn-success btn-sm px-3" href="request.html?id=${element['id']}" data-mdb-toggle="tooltip" data-mdb-placement="bottom" title="Podgląd"><i class="far fa-eye"></i></a><a type="button" class="btn btn-success btn-sm px-3" href="edit_request.html?id=${element['id']}" data-mdb-toggle="tooltip" data-mdb-placement="bottom" title="Edytuj"><i class="fas fa-edit"></i></a><button type="button" class="btn btn-success btn-sm px-3" data-mdb-toggle="tooltip" data-mdb-placement="bottom" title="..."><i class="fas fa-ellipsis-h"></i></button></td></tr>`
        } else {
            content += `<tr class="data_row`;
            if (default_hidden.indexOf(element['status']) !== -1 && !$('#request_gone').val()) {
                content += ' hidden';
            }
            content += `" data-status="${element['status']}"><td>${element['id']}</td><td>${element['date0']}</td><td>${element['date1']}</td><td>${element['customer']}</td><td>${element['item']}</td><td>${statuses[element['status']]}</td><td><a type="button" class="btn btn-success btn-sm px-3" href="request.html?id=${element['id']}" data-mdb-toggle="tooltip" data-mdb-placement="bottom" title="Podgląd"><i class="far fa-eye"></i></a><a type="button" class="btn btn-success btn-sm px-3" href="edit_request.html?id=${element['id']}" data-mdb-toggle="tooltip" data-mdb-placement="bottom" title="Edytuj"><i class="fas fa-edit"></i></a><button type="button" class="btn btn-success btn-sm px-3" data-mdb-toggle="tooltip" data-mdb-placement="bottom" title="..."><i class="fas fa-ellipsis-h"></i></button></td></tr>`
        }
    });
    content += `</tbody></table>`
    return content
}

function columnRequestParser(data, editable=false) {
    let content = '<form>';
    let dict_keys = Object.keys(data);
    dict_keys.forEach(element => {
        content += `<div class="row mt-4"><div class="col-md"></div><div class="col-md">`;
        if (element === 'employee' || element === 'customer') {
            if (editable && element === 'employee') {
                content += `<label class="form-label" for="${element}">${requests_keys_map[element]}</label><select id="${element}" class="form-select" name="${element}" data-value="${data[element]['id']}">`
                content += `</select></div><div class="col-md"></div></div>`
            } else {
                content += `<div class="form-outline"><input type="text" name="${element}" class="form-control active" id="${element}" readonly="readonly" value="${data[element]['name']} -- ${data[element]['phone_number']}"/>`;
                content += `<label class="form-label" for="${element}">${requests_keys_map[element]}</label></div></div><div class="col-md"></div></div>`;
            }
        } else {
            if (element !== 'status' || !editable) {
                content += `<div class="form-outline">`
                switch (element) {
                    case 'description':
                        content += `<textarea name="${element}" class="`;
                        break;
                    case 'id':
                        content += `<input type="text" name="${element}_entity" class="`;
                        break;
                    default:
                        content += `<input type="text" name="${element}" class="`;
                }
                content += `form-control active" id="${element}"`;
                if (!editable || element === 'id' || element === 'customer' || element === 'date0' || element === 'date1' || element === 'date2' || element === 'item') {
                    content += ' readonly="readonly"'
                }
                if (element !== 'status' && element !== 'price') {
                    content += element === 'description' ? `>${data[element]}</textarea> ` : `value="${data[element]}"/>`
                } else if (element === 'price') {
                    content += (data[element] !== null) ? `value="${data[element]}"/>` : `value="0"/>`
                } else {
                    content += `value="${statuses[data[element]]}"/>`
                }
                content += `<label class="form-label" for="${element}">${requests_keys_map[element]}</label></div></div><div class="col-md"></div></div>`;
            } else {
                content += `<label class="form-label" for="${element}">${requests_keys_map[element]}</label><select class="form-select mb-4" name="${element}">`
                let statuses_keys = Object.keys(statuses);
                statuses_keys.forEach(element_status => {
                    content += `<option value=${element_status}`
                    content += parseInt(element_status) === data[element] ? ' selected' : ''
                    content += `>${statuses[element_status]}</option>`
                })
                content += `</select></div><div class="col-md"></div></div>`
            }
        }
    })
    content += editable ? `<div class="row mt-4"><div class="col-md"></div><div class="col-md"><div class="form-outline"><button type="button" class="btn btn-primary btn-block mb-4" id="department_apply" onclick="update_data(this.form, 'request')">Wyślij</button></div></button></div><div class="col-md"></div></div></form>`: '</form>'
    return content;
}

function getRequestsByDate(scope1, date1=null, date2=null) {
    let date_from = (date1 == null) ? '' : '&date_from1='+date1;
    let date_to = (date2 == null) ? '' : '&date_to1='+date2;
    let token = getCookie('authorization');
    let scope = (scope1 === 'dash') ? '?scope='+parseJwt(token)['username'] : '';
    let timeout = setTimeout(function() {$('#query_result').html('<button type="button" class="btn btn-danger" disabled>Błąd połączenia z API</button>')}, api_gui_timeout);
    fetch(`${api_url}/get/requests_date${scope}${date_from}${date_to}`, {method: "GET", mode: "cors", headers: {'authorization': token}})
        .then((resp) => {
            if (resp.status === 400) {
                clearTimeout(timeout);
                $('#query_result').html('<button type="button" class="btn btn-danger" disabled>Problem z zakresem dat</button>');
            } else if (resp.status === 404) {
                clearTimeout(timeout);
                $('#query_result').html('<button type="button" class="btn btn-warning" disabled>Brak wyników dla twojego zapytania</button>');
            } else if (resp.status >= 200 && resp.status <= 299) {
                return resp.json();
            } else {
                clearTimeout(timeout);
                $('#query_result').html('<button type="button" class="btn btn-danger" disabled>Unexpected error</button>');
            }
        })
        .then((data) => {
            if (data !== undefined) {
                clearTimeout(timeout);
                $('#query_result').html(tableParserReq(data));
            }
        })
        .catch(function(error) {
            clearTimeout(timeout);
            $('#query_result').html('<button type="button" class="btn btn-danger" disabled>Unexpected error</button>');
            console.log(error);
        });
}

function getRequestById(id, editable=false) {
    if (isNaN(id)) {
        $('#query_result').html('<button type="button" class="btn btn-danger" disabled>Request ID is NaN (Not a Number)</button>')
        return;
    }
    let token = getCookie('authorization');
    let timeout = setTimeout(function() {$('#query_result').html('<button type="button" class="btn btn-danger" disabled>Błąd połączenia z API</button>')}, api_gui_timeout);
    fetch(`${api_url}/get/request/${id}`, {method: "GET", mode: "cors", headers: {'authorization': token}})
        .then((resp) => {
            if (resp.status === 404) {
                clearTimeout(timeout);
                $('#query_result').html('<button type="button" class="btn btn-warning" disabled>Brak wyników dla twojego zapytania</button>');
            } else if (resp.status >= 200 && resp.status <= 299) {
                return resp.json();
            } else {
                console.log(resp.status);
                clearTimeout(timeout);
                $('#query_result').html('<button type="button" class="btn btn-danger" disabled>Unexpected error</button>');
            }
            console.log(resp)
        })
        .then((data) => {
            if (data !== undefined) {
                clearTimeout(timeout);
                $('#query_result').html(columnRequestParser(data, editable));
                if (editable) {
                    getEmployees($('#employee'));
                }
            }
        })
        .catch(function(error) {
            clearTimeout(timeout);
            $('#query_result').html('<button type="button" class="btn btn-danger" disabled>Unexpected error</button>');
            console.log(error);
        });
}

function getDashboardData(scope) {
    let date_from = $('#dateFrom').val();
    let date_to = $('#dateTo').val();
    getRequestsByDate(scope, date_from, date_to);
}

function tableParserCustomer(data) {
    let content = `<table class="table align-middle"><thead><tr><th scope="col">Id</th><th scope="col">Imię i nazwisko</th><th scope="col">telefon</th><th scope="col">Email</th><th scope="col">Akcje</th></tr></thead><tbody>`
    data.forEach(element => {
        content += `<tr class="data_row"><td>${element['id']}</td><td>${element['name']}</td><td>${element['phone_number']}</td><td>${element['email']}</td><td><a type="button" class="btn btn-success btn-sm px-3" href="customer.html?id=${element['id']}" data-mdb-toggle="tooltip" data-mdb-placement="bottom" title="Podgląd"><i class="far fa-eye"></i></a><a type="button" class="btn btn-success btn-sm px-3" href="edit_customer.html?id=${element['id']}" data-mdb-toggle="tooltip" data-mdb-placement="bottom" title="Edytuj"><i class="fas fa-edit"></i></a><a type="button" class="btn btn-success btn-sm px-3" data-mdb-toggle="tooltip" data-mdb-placement="bottom" title="Zlecenia"><i class="fas fa-list"></i></i></a></td></tr>`
    });
    content += `</tbody></table>`
    return content
}

function getAllCustomers() {
    let token = getCookie('authorization');
    let timeout = setTimeout(function() {$('#query_result').html('<button type="button" class="btn btn-danger" disabled>Błąd połączenia z API</button>')}, api_gui_timeout);
    fetch(`${api_url}/get/customers`, {method: "GET", mode: "cors", headers: {'authorization': token}})
        .then((resp) => {
            if (resp.status >= 200 && resp.status <= 299) {
                return resp.json();
            } else {
                clearTimeout(timeout);
                $('#query_result').html('<button type="button" class="btn btn-danger" disabled>Unexpected error</button>');
            }
        })
        .then((data) => {
            if (data !== undefined) {
                clearTimeout(timeout);
                $('#query_result').html(tableParserCustomer(data));
            }
        })
        .catch(function(error) {
            clearTimeout(timeout);
            $('#query_result').html('<button type="button" class="btn btn-danger" disabled>Unexpected error</button>');
            console.log(error);
        });
}

function columnCustomerParser(data, editable=false) {
    let content = '<form>';
    let dict_keys = Object.keys(data);
    dict_keys.forEach(element => {
        content += `<div class="row mt-4"><div class="col-md"></div><div class="col-md"><div class="form-outline">`;
        content += `<input type="text" class="form-control active" id="${element}"`;
        content += element === 'id' ? ` name="${element}_entity"` : ` name="${element}"`
        if (!editable || element === 'id') {
            content += ' readonly="readonly"'
        }
        content += `value="${data[element]}"/><label class="form-label" for="${element}">${customers_keys_map[element]}</label></div></button></div><div class="col-md"></div></div>`;
    })
    content += editable ? `<div class="row mt-4"><div class="col-md"></div><div class="col-md"><div class="form-outline"><button type="button" class="btn btn-primary btn-block mb-4" id="department_apply" onclick="update_data(this.form, 'customer')">Wyślij</button></div></button></div><div class="col-md"></div></div></form>`: '</form>'
    return content;
}

function getCustomerById(id, editable) {
    if (isNaN(id)) {
        $('#query_result').html('<button type="button" class="btn btn-danger" disabled>Request ID is NaN (Not a Number)</button>')
        return;
    }
    let token = getCookie('authorization');
    let timeout = setTimeout(function() {$('#query_result').html('<button type="button" class="btn btn-danger" disabled>Błąd połączenia z API</button>')}, api_gui_timeout);
    fetch(`${api_url}/get/customer/${id}`, {method: "GET", mode: "cors", headers: {'authorization': token}})
        .then((resp) => {
            if (resp.status === 404) {
                clearTimeout(timeout);
                $('#query_result').html('<button type="button" class="btn btn-warning" disabled>Brak wyników dla twojego zapytania</button>');
            } else if (resp.status >= 200 && resp.status <= 299) {
                return resp.json();
            } else {
                console.log(resp.status);
                clearTimeout(timeout);
                $('#query_result').html('<button type="button" class="btn btn-danger" disabled>Unexpected error</button>');
            }
            console.log(resp)
        })
        .then((data) => {
            if (data !== undefined) {
                clearTimeout(timeout);
                $('#query_result').html(columnCustomerParser(data, editable));
            }
        })
        .catch(function(error) {
            clearTimeout(timeout);
            $('#query_result').html('<button type="button" class="btn btn-danger" disabled>Unexpected error</button>');
            console.log(error);
        });
}
function tableParserEmployee(data) {
    let content = `<table class="table align-middle"><thead><tr><th scope="col">Id</th><th scope="col">Imię i nazwisko</th><th scope="col">telefon</th><th scope="col">Email</th><th scope="col">Akcje</th></tr></thead><tbody>`
    data.forEach(element => {
        if (element !== 'password') {
            content += `<tr class="data_row"><td>${element['id']}</td><td>${element['name']}</td><td>${element['phone_number']}</td><td>${element['email']}</td><td><a type="button" class="btn btn-success btn-sm px-3" href="employee.html?id=${element['id']}" data-mdb-toggle="tooltip" data-mdb-placement="bottom" title="Podgląd"><i class="far fa-eye"></i></a><a type="button" class="btn btn-success btn-sm px-3" href="edit_employee.html?id=${element['id']}" data-mdb-toggle="tooltip" data-mdb-placement="bottom" title="Edytuj"><i class="fas fa-edit"></i></a><a type="button" class="btn btn-success btn-sm px-3" data-mdb-toggle="tooltip" data-mdb-placement="bottom" title="Zlecenia"><i class="fas fa-list"></i></i></a></td></tr>`
        }
    });
    content += `</tbody></table>`
    return content
}

function getAllEmployees() {
    let token = getCookie('authorization');
    let timeout = setTimeout(function() {$('#query_result').html('<button type="button" class="btn btn-danger" disabled>Błąd połączenia z API</button>')}, api_gui_timeout);
    fetch(`${api_url}/get/employees`, {method: "GET", mode: "cors", headers: {'authorization': token}})
        .then((resp) => {
            if (resp.status >= 200 && resp.status <= 299) {
                return resp.json();
            } else {
                clearTimeout(timeout);
                $('#query_result').html('<button type="button" class="btn btn-danger" disabled>Unexpected error</button>');
            }
        })
        .then((data) => {
            if (data !== undefined) {
                clearTimeout(timeout);
                $('#query_result').html(tableParserEmployee(data));
            }
        })
        .catch(function(error) {
            clearTimeout(timeout);
            $('#query_result').html('<button type="button" class="btn btn-danger" disabled>Unexpected error</button>');
            console.log(error);
        });
}

function columnEmployeeParser(data, editable=false) {
    let content = '<form>';
    let dict_keys = Object.keys(data);
    dict_keys.forEach(element => {
        if (element !== 'password' && element !== 'token') {
            if (element !== 'admin_permissions' && element !== 'activated' && (element !== 'department' || !editable)) {
                content += `<div class="row mt-4"><div class="col-md"></div><div class="col-md"><div class="form-outline">`;
                content += `<input type="text" class="form-control active" id="${element}"`;
                content += element === 'id' ? ` name="${element}_entity"` : ` name="${element}"`
                if (!editable || element === 'id' || element === 'username') {
                    content += ' readonly="readonly" '
                }
                content += (element === 'department') ? `value="${data[element]['name']}"` : `value="${data[element]}"`
                content += `/><label class="form-label" for="${element}">${employees_keys_map[element]}</label></div></button></div><div class="col-md"></div></div>`;
            } else if (element === 'department') {
                content += `<div class="row mt-4"><div class="col-md"></div><div class="col-md"><div class="form-outline"><label class="form-label" for="${element}">${employees_keys_map[element]}</label><select id="${element}" class="form-select" name="${element}" data-value="${data[element]['id']}"></select></div></div><div class="col-md"></div></div>`;
            } else {
                switch (element) {
                    case 'activated':
                        content += `<div class="row mt-4"><div class="col-md"></div><div class="col-md"><div class="form-check mb-4"><input class="form-check-input" type="checkbox" value="" id="${element}" name="${element}"`
                        content += (data[element]) ? 'checked' : '';
                        content += (!editable) ? ' onclick="return false;"' : '';
                        content += `/><label class="form-check-label" for="${element}">Konto ma być aktywne?</label></div></div><div class="col-md"></div></div>`
                        break;
                    case 'admin_permissions':
                        content += `<div class="row mt-4"><div class="col-md"></div><div class="col-md"><div class="form-check mb-4"><input class="form-check-input" type="checkbox" value="" id="${element}"`
                        content += (data[element]) ? 'checked' : '';
                        content += (!editable || !parseJwt(getCookie('authorization'))['admin']) ? ' onclick="return false;"' : ` name="${element}"`;
                        content += `/><label class="form-check-label" for="${element}">Czy admin?</label></div></div><div class="col-md"></div></div>`
                        break;
                    default:
                        console.log('something went wrong');
                }
            }
        }
    })
    content += editable ? `<div class="row mt-4"><div class="col-md"></div><div class="col-md"><div class="form-outline"><button type="button" class="btn btn-primary btn-block mb-4" id="department_apply" onclick="update_data(this.form, 'employee')">Wyślij</button></div></button></div><div class="col-md"></div></div></form>`: '</form>'
    return content;
}

function getEmployee(id, editable) {
    if (isNaN(id)) {
        $('#query_result').html('<button type="button" class="btn btn-danger" disabled>Request ID is NaN (Not a Number)</button>')
        return;
    }
    let token = getCookie('authorization');
    let timeout = setTimeout(function() {$('#query_result').html('<button type="button" class="btn btn-danger" disabled>Błąd połączenia z API</button>')}, api_gui_timeout);
    fetch(`${api_url}/get/employee/${id}`, {method: "GET", mode: "cors", headers: {'authorization': token}})
        .then((resp) => {
            if (resp.status === 404) {
                clearTimeout(timeout);
                $('#query_result').html('<button type="button" class="btn btn-warning" disabled>Brak wyników dla twojego zapytania</button>');
            } else if (resp.status >= 200 && resp.status <= 299) {
                return resp.json();
            } else {
                console.log(resp.status);
                clearTimeout(timeout);
                $('#query_result').html('<button type="button" class="btn btn-danger" disabled>Unexpected error</button>');
            }
            console.log(resp)
        })
        .then((data) => {
            if (data !== undefined) {
                clearTimeout(timeout);
                $('#query_result').html(columnEmployeeParser(data, editable));
                if (editable) {
                    getEmployees($('#department'));
                }

            }
        })
        .catch(function(error) {
            clearTimeout(timeout);
            $('#query_result').html('<button type="button" class="btn btn-danger" disabled>Unexpected error</button>');
            console.log(error);
        });
}