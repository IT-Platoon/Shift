<template>
  <h5 class="mb-4">Предыдущие запросы</h5>
  <div class="my-3">
    <label for="formFile" class="form-label">Создать запрос</label>
    <input
      class="form-control"
      type="file"
      id="formFile"
      @change="this.getFile"
    >
  </div>
  <div v-if="this.responses.length">
    <div class="accordion" id="accordionFlushExample">
      <ResponseItem
        v-for="response of this.responses"
        :key="response.id"
        :response="response"
      />
    </div>
  </div>
  <div v-else>
      <h6>Список пуст</h6>
  </div>
</template>

<script>
import ResponseItem from "./ResponseItem.vue";

export default {
  name: "ListResponses",
  components: {
    ResponseItem,
  },
  props: {
    responses: {
      type: Array,
      required: true,
    },
  },
  emits: [
    "createModelProcess",
  ],
  methods: {
    getFile(e) {
      if (e.target.files.length === 1) {
        this.$emit("createModelProcess", e.target.files[0])
      }
    },
  },
};
</script>

<style scoped>
.bgc {
  background-color: #ced4da;
}

.request-title {
  border-radius: 10px !important;
}
</style>