<template>
  <div class="col-md-6 p-0">
    <div class="card m-2 item-card">
      <div class="card-header item-header">
        <h4 class="m-0">{{project.name}}</h4>
      </div>
      <div class="card-body item-body">
        <div v-if="project.consists">
          <button
            class="btn btn-gray"
            @click="$router.push({name: 'project', params: {projectId: project.id}})"
          >
            Перейти на страницу проекта
          </button>
        </div>
        <div v-else-if="project.send_request">
          <button
            class="btn btn-danger"
            @click="sendRemoveRequestToEnter"
          >
            Отменить запрос на вход
          </button>
        </div>
        <div v-else>
          <button
            class="btn btn-gray"
            @click="sendRequestToEnter"
          >
            Отправить запрос на вход
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ProjectService from "../services/project.service.js";

export default {
  name: "ProjectItem",
  props: {
    project: {
      type: Object,
      required: true,
    },
  },
  methods: {
    async sendRequestToEnter() {
      let response = await ProjectService.postWantEnterToProject(this.project.id);
      if (response.status === 200) {
        this.project.send_request = !this.project.send_request 
      }
    },
    async sendRemoveRequestToEnter() {
      let response = await ProjectService.postRemoveRequestToProject(this.project.id);
      if (response.status === 200) {
        this.project.send_request = !this.project.send_request;
      }
    },
  },
};
</script>

<style scoped>
.card-header.item-header {
  background-color: var(--bs-gray-400);
}
.card.item-card {
  background-color: var(--bs-white);
}
.btn.btn-gray {
  background-color: var(--bs-gray-600);
  color: var(--bs-white);
}
</style>
