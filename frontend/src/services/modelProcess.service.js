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

  getModelProcessFile(modelProcessId) {
    return api.get(
      `${this.baseUrl}${modelProcessId}/`,
      {
        responseType: 'arraybuffer',
        headers: {
          "Content-Type": "application/x-gzip",
        },
      },
    ).then((response) => {
      console.log(response)
      let blob = new Blob(
        [response.data],
        { type: 'application/vnd.ms-excel' }
      )
      let url = window.URL.createObjectURL(blob)
      window.open(url);
    });
  }
}

export default new ModelProcessService();
