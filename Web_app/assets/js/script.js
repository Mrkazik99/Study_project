function update_field (datalist, text_input, select) {
    let dataset = $(`#${datalist}`).children();
    console.log(dataset);
    for (let i = 0; i < dataset.length; i++) {
        if (dataset[i].getAttribute('value') === select.value) {
            $(`#${text_input}`).val(dataset[i].innerHTML);
            break;
        }
    }
}

function tableParser(data) {
    let content = `<table class="table align-middle"><thead><tr><th scope="col">Data przyjęcia</th><th scope="col">Data aktualizacji</th><th scope="col">Klient</th><th scope="col">Stan</th><th scope="col">Akcje</th></tr></thead><tbody>`
    data.forEach(element => {
        // if (new Date() - element['date0'] >= 2592000000 || new Date() - element['date1'] >= 2592000000){
        if (new Date() - new Date(element['date0']) >= 86400000 || new Date() - new Date(element['date1']) >= 86400000){
            content += `<tr class="table-danger"><td>${element['date0']}</td><td>${element['date1']}</td><td>${element['customer']}</td><td>${statuses[element['status']]}</td><td><a type="button" class="btn btn-success btn-sm px-3" href="request.html?id=${element['id']}"><i class="far fa-eye"></i></a><a type="button" class="btn btn-success btn-sm px-3" href="edit_request.html?id=${element['id']}"><i class="fas fa-edit"></i></a><button type="button" class="btn btn-success btn-sm px-3"><i class="fas fa-ellipsis-h"></i></button></td></tr>`
        } else {
            content += `<tr><td>${element['date0']}</td><td>${element['date1']}</td><td>${element['customer']}</td><td>${statuses[element['status']]}</td><td><a type="button" class="btn btn-success btn-sm px-3" href="request.html?id=${element['id']}"><i class="far fa-eye"></i></a><a type="button" class="btn btn-success btn-sm px-3" href="edit_request.html?id=${element['id']}"><i class="fas fa-edit"></i></a><button type="button" class="btn btn-success btn-sm px-3"><i class="fas fa-ellipsis-h"></i></button></td></tr>`
        }
    });
    content += `</tbody></table>`
    return content
}

function columnParser(data, editable=false) {
    cos = data.keys
    cos.forEach(element => {console.log(element)})
    let content = `
    <div class="row mt-4">
        <div class="col-md"></div>
        <div class="col-md">
            <div class="form-outline">
                <input type="text" id="customer_name" class="form-control active" disabled value="${data['customer']}"/>
                <label class="form-label" for="customer_name">Klient</label>
            </div>
            </button>
        </div>
        <div class="col-md"></div>
    </div>
    <div class="row mt-4">
        <div class="col-md"></div>
        <div class="col-md">
            <div class="form-outline">
                <input type="text" id="employee_name" class="form-control active" disabled value="${data['employee']}"/>
                <label class="form-label" for="employee_name">Serwisant</label>
            </div>
            </button>
        </div>
        <div class="col-md"></div>
    </div>
    <div class="row mt-4">
        <div class="col-md"></div>
        <div class="col-md">
            <div class="form-outline">
                <textarea class="form-control active" id="description" rows="4" disabled>${data['description']}</textarea>
                <label class="form-label" for="description">Opis</label>
            </div>
            </button>
        </div>
        <div class="col-md"></div>
    </div>
    <div class="row mt-4">
        <div class="col-md"></div>
        <div class="col-md">
            <div class="form-outline">
                <input type="text" id="date0" class="form-control active" disabled value="${data['date0']}"/>
                <label class="form-label" for="date0">Data przyjęcia</label>
            </div>
            </button>
        </div>
        <div class="col-md"></div>
    </div>
    <div class="row mt-4">
        <div class="col-md"></div>
        <div class="col-md">
            <div class="form-outline">
                <input type="text" id="date1" class="form-control active" disabled value="${data['date1']}"/>
                <label class="form-label" for="date1">Data ostatniej aktualizacji</label>
            </div>
            </button>
        </div>
        <div class="col-md"></div>
    </div>
    <div class="row mt-4">
        <div class="col-md"></div>
        <div class="col-md">
            <div class="form-outline">
                <input type="text" id="date2" class="form-control active" disabled value="${data['date2']}"/>
                <label class="form-label" for="date2">Data wydania</label>
            </div>
            </button>
        </div>
        <div class="col-md"></div>
    </div>
    <div class="row mt-4">
        <div class="col-md"></div>
        <div class="col-md">
            <div class="form-outline">
                <input type="text" id="price" class="form-control active" disabled value="${data['price']} PLN"/>
                <label class="form-label" for="price">Wycena</label>
            </div>
            </button>
        </div>
        <div class="col-md"></div>
    </div>
    `
    return content
}

function getRequestsByDate(date1=null, date2=null) {
    let date_from = (date1 == null) ? '' : '?date_from=';
    let date_to = (date2 == null) ? '' : '&date_to=';
    console.log(date_from, date_to)
    let timeout = setTimeout(function() {$('#query_result').html('<button type="button" class="btn btn-danger" disabled>Błąd połączenia z API</button>')}, 5000);
    fetch(`${api_url}/get/requests_date${date_from}${date_to}`, {method: "GET", mode:"cors"})
        .then((resp) => {
            console.log(resp)
            if (resp.status === 400) {
                console.log('400 error');
                clearTimeout(timeout);
                $('#query_result').html('<button type="button" class="btn btn-danger" disabled>Problem z zakresem dat</button>');
            } else if (resp.status === 404) {
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
                $('#query_result').html(tableParser(data));
                console.log(data);
            }
        })
        .catch(function(error) {
            clearTimeout(timeout);
            $('#query_result').html('<button type="button" class="btn btn-danger" disabled>Unexpected error</button>');
            console.log(error);
        });
}

function getRequestById(id) {
    if (isNaN(id)) {
        $('#query_result').html('<button type="button" class="btn btn-danger" disabled>Request ID is NaN (Not a Number)</button>')
        return;
    }
    let timeout = setTimeout(function() {$('#query_result').html('<button type="button" class="btn btn-danger" disabled>Błąd połączenia z API</button>')}, 5000);
    fetch(`${api_url}/get/request/${id}`, {method: "GET", mode: "cors"})
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
                $('#query_result').html(columnParser(data, false));
                // $('#query_result').text(JSON.stringify(data));
                console.log(data);
            }
        })
        .catch(function(error) {
            clearTimeout(timeout);
            $('#query_result').html('<button type="button" class="btn btn-danger" disabled>Unexpected error</button>');
            console.log(error);
        });
}

//to jest tylko przykładowa funkcja (do poprawienia lub wyjebania)

// function create_new_customer() {
//     $("#customer_form")
//     let customer_infos = {
//         'name': `${form.name} ${customer.surname}`,
//         'phone': form.phone,
//         'mail': form.mail
//     };
//     payload = JSON.parse(customer_infos);
// }