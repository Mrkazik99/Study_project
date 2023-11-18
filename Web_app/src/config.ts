export const api_url = "http://localhost:20001";
export const api_gui_timeout = 5000; //[ms]
export const default_hidden = [4];
export const token_time = 9999;
export const statuses = {
  0: "...",
  1: "Nowy",
  2: "W trakcie naprawy",
  3: "On hold",
  4: "Zakończone",
};
export const requests_keys_map = {
  id: "Id",
  employee: "Serwisant",
  customer: "Klient",
  description: "Opis",
  item: "Przedmiot",
  status: "Status",
  date0: "Data przyjęcia",
  date1: "Data ostatniej aktualziacji",
  date2: "Data wydania",
  price: "Wycena",
};
export const customers_keys_map = {
  id: "Id",
  name: "Imię i nazwisko",
  phone_number: "Telefon",
  email: "Email",
};
export const employees_keys_map = {
  id: "Id",
  username: "Login",
  email: "Email",
  password: "Hasło",
  department: "Dział",
  activated: "Czy aktywne",
  admin_permissions: "Czy admin",
  name: "Imię i nazwisko",
  phone_number: "Telefon",
};
