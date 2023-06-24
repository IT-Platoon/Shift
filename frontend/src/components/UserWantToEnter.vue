<template>
    <div class="radius card mb-2">
        <div class="p-2 d-flex flex-row justify-content-between align-items-center">
            <div class="card-body">
                <h5 class="m-0">{{ user.username }}</h5>
                <p class="card-text">
                    {{ user.first_name }} {{ user.last_name }}
                </p>
            </div>
            <button
                class="btn btn-success"
                @click="this.addMember"
            >
                Принять
            </button>
            <button
                class="btn btn-danger ms-2"
                @click="this.removeWantToEnter"
            >
                Отклонить
            </button>
        </div>
    </div>
</template>

<script>
export default {
  name: "UserWantToEnter",
  props: {
    user: {
      type: Object,
      required: true,
    },
  },
  emits: [
    "emitAddMember",
    "emitRemoveWantToEnter",
  ],
  methods: {
    async addMember() {
        this.$emit("emitAddMember", this.user.id)
    },
    async removeWantToEnter() {
        this.$emit("emitRemoveWantToEnter", this.user.id)
    },
  }
};
</script>

<style scoped>
.radius {
    border-radius: 10px;
}
</style>
