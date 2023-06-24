import axiosInstance from "./api";
import TokenService from "./token.service";

const setup = (store) => {
  axiosInstance.interceptors.request.use(
    (config) => {
      const token = TokenService.getLocalAccessToken();
      if (token) {
        config.headers["Authorization"] = 'JWT ' + token;
      }
      return config;
    },
    // (error) => {
    //   return Promise.reject(error);
    // }
  );

  axiosInstance.interceptors.response.use(
    (res) => {
      return res;
    },
    async (err) => {
      const originalConfig = err.config;

      if (originalConfig.url !== "token/" && err.response) {
        if (err.response.status === 401 && !originalConfig._retry) {
          originalConfig._retry = true;

          try {
            const rs = await axiosInstance.post("token/refresh/", {
              refreshToken: TokenService.getLocalRefreshToken(),
            });

            const { access } = rs.data;

            store.dispatch('token/refresh/', access);
            TokenService.updateLocalAccessToken(access);

            return axiosInstance(originalConfig);
          } catch (_error) {
            localStorage.clear()
            return null;
          }
        }
      }

      return Promise.reject(err);
    }
  );
};

export default setup;