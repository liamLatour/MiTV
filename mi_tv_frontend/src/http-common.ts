import axios from "axios";

export const backendURL = "http://127.0.0.1:5000/"; //"http://backend:5000/";

export default axios.create({
  baseURL: backendURL,
});