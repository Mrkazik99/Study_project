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

statuses = {
    0: '...',
    1: 'Nowy',
    2: 'W trakcie naprawy',
    3: 'On hold'
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