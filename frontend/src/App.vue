<template>
  <div id="app">
    <nav class="navbar navbar-expand navbar-dark bg-dark d-flex justify-content-between">
      <div class="navbar-nav">
        <li class="nav-item">
          <router-link to="/" class="nav-link">
            Домашняя страница
          </router-link>
        </li>
        <li class="nav-item">
          <router-link v-if="currentUser" to="/profile" class="nav-link">
            Профиль
          </router-link>
        </li>
      </div>

      <div v-if="!currentUser" class="navbar-nav">
        <li class="nav-item">
          <router-link to="/register" class="nav-link">
            Регистрация
          </router-link>
        </li>
        <li class="nav-item">
          <router-link to="/login" class="nav-link">
            Вход
          </router-link>
        </li>
      </div>

      <div v-if="currentUser" class="navbar-nav">
        <li class="nav-item">
          <router-link to="/profile" class="nav-link">
            {{ currentUser?.username }}
          </router-link>
        </li>
        <li class="nav-item">
          <a class="nav-link" @click.prevent="logOut">
            Выход
          </a>
        </li>
      </div>
    </nav>

    <div class="container">
      <router-view />
    </div>
  </div>
</template>

<script>
import EventBus from "./common/EventBus";

export default {
  computed: {
    currentUser() {
      return this.$store.state.auth.user;
    },
  },
  methods: {
    logOut() {
      this.$router.push('/login');
      this.$store.dispatch('auth/logout');
    }
  },
  mounted() {
    EventBus.on("logout", () => {
      this.logOut();
    });
  },
  beforeUnmount() {
    EventBus.remove("logout");
  }
};
</script>
