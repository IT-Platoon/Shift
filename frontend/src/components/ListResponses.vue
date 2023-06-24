<template>
    <h5>Предыдущие запросы</h5>
    <input
      class="my-3"
      @change="this.getFile"
      type="file"
      id="formFile"
    />
    <div v-if="this.responses.length">
        <div class="accordion accordion-flush" id="accordionFlushExample">
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
  }
};
</script>