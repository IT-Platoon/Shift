import api from "./api";
import TokenService from "./token.service";

class AuthService {
  login({ username, password }) {
    return api
      .post("token/", {
        username,
        password
      })
      .then((response) => {
        if (response.data.access) {
          TokenService.setToken(response.data);
        }

        return api
        .get("users/me/")
        .then((response) => {   
          if (response.data.id) {
            return response.data;
          }       
        });
      });
  }

  logout() {
    TokenService.removeTokens();
  }

  register({ username, first_name, last_name, email, password }) {
    return api.post("users/", {
      username,
      first_name,
      last_name,
      email,
      password,
    });
  }
}

export default new AuthService();
