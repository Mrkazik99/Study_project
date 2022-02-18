const api_url = 'http://127.0.0.1:20001';
const statuses = {
        0: '...',
        1: 'Nowy',
        2: 'W trakcie naprawy',
        3: 'On hold',
        4: 'Zakończone'
    };
const requests_keys_map ={
    'id': 'Id',
    'employee': 'Serwisant',
    'customer': 'Klient',
    'description': 'Opis',
    'status': 'Status',
    'date0': 'Data przyjęcia',
    'date1': 'Data ostatniej aktualziacji',
    'date2': 'Data wydania',
    'price': 'Wycena',
}
const customers_keys_map ={
}
const employees_keys_map ={
}
const api_gui_timeout = 5000; //[ms]
const default_hidden = [4];