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
    <div class="text-center">
      <div v-if="this.response.graphic && 'labels' in this.response.graphic">
        <Line :data="this.response.graphic"/>
      </div>
      <div class="text-center" v-else>График еще не сгенерирован</div>
    </div>
    </div>
  </div>
</template>

<script>
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
  data() {
    return {
      data: {},
      condition: false,
    }
  },
  mounted() {
    this.condition = this.response.graphic  && 'labels' in this.response.graphic
    this.data = this.response.graphic 
  }
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