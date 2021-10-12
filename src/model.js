import { action } from "easy-peasy";

const getSavedStorage = (key) => {
  return JSON.parse(window.localStorage.getItem(key)) || initial[key];
};

const setSavedStorage = (key, obj) => {
  window.localStorage.setItem(key, JSON.stringify(obj));
};

const initial = {
  points: [],
  file: "",
};

export default {
  points: getSavedStorage("points"),
  setPoints: action((state, points) => {
    state.points = [...points];
    setSavedStorage("points", points);
  }),
  file: getSavedStorage("file"),
  setFile: action((state, file) => {
    state.file = [...file];
    setSavedStorage("file", file);
  }),
};
