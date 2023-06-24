import api from './api';

class ProjectService {
  baseUrl = 'projects/'

  getListProjects() {
    return api.get(this.baseUrl);
  }

  postWantEnterToProject(projectId) {
    return api.post(`${this.baseUrl}${projectId}/want-enter/`);
  }

  postRemoveRequestToProject(projectId) {
    return api.post(`${this.baseUrl}${projectId}/cancel-want-enter/`);
  }

  getProjectInfo(projectId) {
    return api.get(`${this.baseUrl}${projectId}/`);
  }

  getProjectMembers(projectId) {
    return api.get(`${this.baseUrl}${projectId}/get-members/`);
  }

  getProjectWantToEnter(projectId) {
    return api.get(`${this.baseUrl}${projectId}/get-want-enter/`);
  }

  getModelProcesses(projectId) {
    return api.get(`${this.baseUrl}${projectId}/responses/`);
  }

  addMemberToProject(data) {
    return api.post(`${this.baseUrl}add-member/`, data=data);
  }

  removeMemberFromProject(data) {
    return api.post(`${this.baseUrl}remove-member/`, data=data);
  }

  removeWantToEnter(data) {
    return api.post(`${this.baseUrl}remove-want-enter/`, data=data);
  }

  leaveFromProject(projectId) {
    return api.post(`${this.baseUrl}${projectId}/leave-project/`);
  }

  searchProject(searchQuery) {
    return api.get(`${this.baseUrl}?search=${searchQuery}`);
  }

  removeProject(projectId) {
    return api.delete(`${this.baseUrl}${projectId}/`);
  }

  createProject(data) {
    return api.post(this.baseUrl, data=data);
  }

  updateProject(projectId, data) {
    return api.patch(`${this.baseUrl}${projectId}/`, data=data);
  }
}

export default new ProjectService();
