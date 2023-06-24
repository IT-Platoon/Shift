import axios from "axios";

const isProduction = process.env.NODE_ENV === "production"
const instance = axios.create({
  baseURL: `http://${isProduction ? 'localhost' : 'localhost:8000'}/api`,
});

export default instance;
