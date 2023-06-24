import axios from "axios";

const isProduction = process.env.NODE_ENV === "production"
const instance = axios.create({
  baseURL: `http://${isProduction ? '31.129.97.140' : 'localhost:8000'}/api`,
});

export default instance;
