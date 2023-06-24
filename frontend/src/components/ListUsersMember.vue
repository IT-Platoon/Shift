<template>
    <h5>Участники</h5>
    <UserMember
        v-for="member of this.members"
        :key="member.id"
        :member="member"
        :isOwner="this.isOwner"
        :ownerId="this.ownerId"
        @emitRemoveMember="removeMember"
    />
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