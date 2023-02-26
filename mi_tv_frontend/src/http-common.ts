import axios from "axios";

export const backendURL = "http://backend:5000/";

export default axios.create({
  baseURL: backendURL,
});