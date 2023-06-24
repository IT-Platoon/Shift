<template>
  <h5 class="mb-4">Хотят присоединиться</h5>
  <div v-if="this.wantToEnterUsers.length">
    <div class="scroll-area overflow-auto">
      <UserWantToEnter
        v-for="user of this.wantToEnterUsers"
        :key="user.id"
        :user="user"
        @emitAddMember="this.addMember"
        @emitRemoveWantToEnter="this.removeWantToEnter"
      />
    </div>
  </div>
  <div v-else>
      <h6>Список пуст</h6>
  </div>
</template>

<script>
import UserWantToEnter from "./UserWantToEnter.vue";

export default {
  name: "ListUsersWantToEnter",
  components: {
    UserWantToEnter,
  },
  props: {
    wantToEnterUsers: {
      type: Array,
      required: true,
    },
  },
  emits: [
    "emitAddMember",
    "emitRemoveWantToEnter",
  ],
  methods: {
    async addMember(userId) {
      this.$emit("emitAddMember", userId)
    },
    async removeWantToEnter(userId) {
      this.$emit("emitRemoveWantToEnter", userId)
    },
  }
};
</script>

<style scoped>
.scroll-area {
  max-height: 150px;
}
</style>