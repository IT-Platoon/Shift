<template>
    <div class="card mb-2">
        <div class="p-2 d-flex flex-row justify-content-between align-items-center">
            <div class="card-body">
                <h5 class="m-0">{{ member?.username }}</h5>
                <p class="card-text">
                    {{ member?.first_name }} {{ member?.last_name }}
                </p>
            </div>
            <div v-if="this.isOwner">
                <div v-if="this.ownerId !== member.id">
                    <button
                        class="btn btn-danger"
                        @click="this.removeMember"
                    >
                        Удалить
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
  name: "UserMember",
  props: {
    member: {
      type: Object,
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
    async removeMember() {
        this.$emit("emitRemoveMember", this.member.id)
    }
  }
};
</script>