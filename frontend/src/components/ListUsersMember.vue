<template>
  <h5 class="mb-4">Участники</h5>
  <div class="scroll-area overflow-auto">
    <UserMember
      v-for="member of this.members"
      :key="member.id"
      :member="member"
      :isOwner="this.isOwner"
      :ownerId="this.ownerId"
      @emitRemoveMember="removeMember"
    />
  </div>
</template>

<script>
import UserMember from "./UserMember.vue";

export default {
  name: "ListUsersMember",
  components: {
    UserMember,
  },
  props: {
    members: {
      type: Array,
      required: true,
    },
    isOwner: {
        type: Boolean,
        required: true,
    },
    ownerId: {
        type: Number,
        required: true,
    },
  },
  emits: [
    "emitRemoveMember",
  ],
  methods: {
    async removeMember(memberId) {
        this.$emit("emitRemoveMember", memberId)
    }
  }
};
</script>

<style scoped>
.scroll-area {
  max-height: 150px;
}
</style>