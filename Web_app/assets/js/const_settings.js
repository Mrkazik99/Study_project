const api_url = 'http://192.168.1.230:20001';
const statuses = {
        0: '...',
        1: 'Nowy',
        2: 'W trakcie naprawy',
        3: 'On hold',
        4: 'Zakończone'
    };
const names_map ={
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
const api_gui_timeout = 5000; //[ms]
const default_hidden = [4];