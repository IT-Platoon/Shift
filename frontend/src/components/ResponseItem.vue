<template>
  <div class="accordion-item request-title mb-2">
    <h2 class="accordion-header request-title" id="flush-headingOne">
      <button
        class="accordion-button collapsed request-title"
        type="button"
        data-bs-toggle="collapse"
        :data-bs-target="'#flush-collapse' + response.id"
        aria-expanded="false"
        aria-controls="flush-collapseOne"
      >
        Запрос от {{ response.created }}
      </button>
      {{ response.graphic }}
      {{ response.tasks }}
    </h2>
    <div
      :id="'flush-collapse' + response.id"
      class="accordion-collapse collapse request-title"
      aria-labelledby="flush-headingOne"
      data-bs-parent="#accordionFlushExample"
    >
    <div class="my-3 d-flex justify-content-around">
      <button
        class="btn bgc"
        @click="downloadRequest"
      >
      <i class="bi bi-download"></i>
        Скачать запрос
      </button>
    </div>
    <div>
      <div v-if="response.tasks && response.graphic && 'labels' in response.graphic">
        <Line :data="response.graphic"/>
        <table class="table">
          <thead>
            <tr>
              <th scope="col">Код задачи</th>
              <th scope="col">Название задачи</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="task of response.tasks" :key="task.code">
              <th scope="row">{{ task.code }}</th>
              <td>{{ task.name }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else>График еще не сгенерирован</div>
    </div>
    </div>
  </div>
</template>

<script>
import ModelProcessService from "../services/modelProcess.service.js";
import { Line } from 'vue-chartjs'
import {Chart as ChartJS, registerables} from 'chart.js'

ChartJS.register(...registerables)

export default {
  name: "ResponseItem",
  components: {
    Line,
  },
  props: {
    response: {
      type: Object,
      required: true,
    },
  },
  methods: {
    async downloadRequest() {
      await ModelProcessService.getModelProcessFile(this.response.id)
    },
  },
};
</script>

<style scoped>
.bgc {
  background-color: #ced4da;
}

.request-title {
  border-radius: 20px;
  border: 1px solid #fff;
  color: #000 !important;
  background-color: #fff !important;
}
</style>