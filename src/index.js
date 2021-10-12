import React from "react";
import ReactDOM from "react-dom";
import "./index.css";
import "animate.css";
import { StoreProvider, createStore } from "easy-peasy";
import App from "./App";
import model from "./model";

const store = createStore(model);

ReactDOM.render(
  <React.StrictMode>
    <StoreProvider store={store}>
      <App />
    </StoreProvider>
  </React.StrictMode>,
  document.getElementById("root")
);
