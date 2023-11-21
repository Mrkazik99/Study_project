import logo from "./logo.svg";
import "./App.css";
import Swal from "sweetalert2";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import Home from "./components/Home/Home";
import Login from "./components/Login/Login";
import CustomerDashboard from "./components/CustomerDashboard/CustomerDashboard";
import NoMatch from "./components/NoMatch/NoMatch";

const App = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route index element={<Home />} />
        <Route path="worker">
          <Route index element={<Login />}></Route>
          <Route path="*" element={<NoMatch />}></Route>
        </Route>
        <Route path="customer">
          <Route index element={<CustomerDashboard />}></Route>
          <Route path="*" element={<NoMatch />}></Route>
        </Route>
        <Route path="*" element={<NoMatch />}></Route>
      </Routes>
    </BrowserRouter>
  );
};

export default App;
