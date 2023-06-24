import { createApp } from "vue";
import ToastPlugin from 'vue-toast-notification';
import 'vue-toast-notification/dist/theme-bootstrap.css';
import App from "./App.vue";
import router from "./router";
import store from "./store";
import "bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";

import setupInterceptors from './services/setupInterceptors';

setupInterceptors(store);

createApp(App)
  .use(router)
  .use(store)
  .use(ToastPlugin)
  .mount("#app");
