import api from './api';

class ModelProcessService {
  baseUrl = 'model-process/'

  createModelProcess(data) {
    return api.post(
      `${this.baseUrl}`,
      data=data,
      {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      },
    );
  }
}

export default new ModelProcessService();
