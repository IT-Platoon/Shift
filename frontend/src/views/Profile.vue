<template>
  <div class="container my-3">
    <p>Никнейм: {{ currentUser?.username }}</p>
    <p>Имя: {{ currentUser?.first_name }}</p>
    <p>Фамилия: {{ currentUser?.last_name }}</p>
    <p>Email: {{ currentUser?.email }}</p>
  </div>
</template>

<script>
export default {
  name: 'Profile',
  computed: {
    currentUser() {
      return this.$store.state.auth.user;
    }
  },
  mounted() {
    if (!this.currentUser) {
      this.$router.push('/login');
    }
  }
};
</script>