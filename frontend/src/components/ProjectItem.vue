<template>
    <div class="card my-4">
        <div class="card-header">
            {{project.name}}
        </div>
        <div class="card-body">
            <div v-if="project.consists">
              <button
                class="btn btn-success"
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
                class="btn btn-primary"
                @click="sendRequestToEnter"
              >
                Отправить запрос на вход
              </button>
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