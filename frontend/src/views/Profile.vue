<template>
  <div class="container card profile my-3 pt-3 pb-1">
    <h5 class="card profile-item p-2">Логин: {{ currentUser?.username }}</h5>
    <h5 class="card profile-item p-2">Имя: {{ currentUser?.first_name }}</h5>
    <h5 class="card profile-item p-2">Фамилия: {{ currentUser?.last_name }}</h5>
    <h5 class="card profile-item p-2">Email: {{ currentUser?.email }}</h5>
  </div>
  <div class="my-3 bgc radius py-3 px-4">
    <h5>Список проектов пользователя</h5>
    <ListProjects
      :projects="this.projects"
    />
  </div>
</template>

<script>
import UserService from "../services/user.service.js";
import ListProjects from "../components/ListProjects.vue";

export default {
  name: 'Profile',
  components: {
    ListProjects,
  },
  data() {
    return {
      projects: [],
    }
  },
  computed: {
    currentUser() {
      return this.$store.state.auth.user;
    }
  },
  methods: {
    async getProjects() {
      let response = await UserService.getUserProjects()
      if (response?.status === 200) {
        this.projects = response.data
      }
    },
  },
  async mounted() {
    if (!this.currentUser) {
      this.$router.push('/login');
    }
    await this.getProjects()
  }
};
</script>

<style>
.bgc {
  background-color: var(--bs-gray-400);;
}

.radius {
  border-radius: 10px !important;
}
.card.profile {
  background-color: var(--bs-gray-400);
  border: none;
  border-radius: 10px;
}
.card.profile-item {
  background-color: var(--bs-white);
}
</style>