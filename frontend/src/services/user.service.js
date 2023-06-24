import api from './api';

class UserService {
    baseUrl = 'users/'

    getUserProjects() {
        return api.get(`${this.baseUrl}projects/`);
    }
}

export default new UserService();
