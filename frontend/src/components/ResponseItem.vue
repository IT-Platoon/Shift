<template>
  <div class="accordion-item">
    <h2 class="accordion-header" id="flush-headingOne">
      <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" :data-bs-target="'#flush-collapse' + response.id" aria-expanded="false" aria-controls="flush-collapseOne">
        Запрос от {{ response.created }}
      </button>
    </h2>
    <div :id="'flush-collapse' + response.id" class="accordion-collapse collapse" aria-labelledby="flush-headingOne" data-bs-parent="#accordionFlushExample">
      <button
        class="btn btn-success"
        @click="downloadRequest"
      >
        Скачать запрос
      </button>
      <div v-for="graphic of response.graphics" :key="graphic[0]">
        <Bar v-if="'labels' in graphic[1]" :data="graphic[1]" />
      </div>
    </div>
  </div>
</template>

<script>
import ModelProcessService from "../services/modelProcess.service.js";
import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, PointElement, LineElement } from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, PointElement, LineElement)

export default {
  name: "ResponseItem",
  components: {
    Bar,
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
    }
  }
};
</script>