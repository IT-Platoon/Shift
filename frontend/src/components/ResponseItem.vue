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
      <div v-for="graphic of response.graphics" :key="graphic[0]">
        <Bar v-if="'labels' in graphic[1]" :data="graphic[1]" />
        <div v-else>График еще не сгенерирован</div>
      </div>
    </div>
  </div>
</template>

<script>
import ModelProcessService from "../services/modelProcess.service.js";
import { Bar } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement
} from 'chart.js'

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
)

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