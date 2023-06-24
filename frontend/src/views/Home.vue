<template>
  <div class="container">
      <div class="input-group my-3">
        <input
          type="text"
          class="form-control"
          placeholder="Введите название проекта"
          v-model="this.searchQuery"
        >
        <button
          class="btn btn-outline-success"
          type="button"
          id="button-addon2"
          @click="this.search"
        >
          Поиск
        </button>
      </div>
      <div>
        <button
          @click="this.openModal"
          class="btn btn-success"
        >
          Создать проект
        </button>
      </div>
      <div class="my-3">
        <ListProjects
          :projects="this.projects"
        />
      </div>
      <ProjectModal
        v-show="this.modal"
        :show="this.modal"
        :project="this.newProject"
        :modalName="this.modalName"
        :buttonLabel="this.buttonLabel"
        @changeProject="this.changeProject"
        @close="closeModal"
      />
  </div>
</template>

<script>
import ProjectService from "../services/project.service.js";
import ListProjects from "../components/ListProjects.vue";
import ProjectModal from "../components/ProjectModal.vue";

export default {
  name: "Home",
  components: {
    ListProjects,
    ProjectModal,
  },
  data() {
    return {
      projects: [],
      searchQuery: "",
      modal: false,
      newProject: {name: ""},
      modalName: "Создать новый проект",
      buttonLabel: "Создать",
    };
  },
  computed: {
    currentUser() {
      return this.$store.state.auth.user;
    },
  },
  methods: {
    openModal() {
      this.modal = !this.modal;
      this.newProject.name = ""
    },
    closeModal() {
      this.modal = !this.modal;
    },
    async changeProject(project) {
      let response = await ProjectService.createProject(project)
      if (response.status === 201) {
        this.projects.push(response.data.project);
        this.$toast.open({
          message: response.data.message,
          type: "success",
          duration: 5000,
        });
      }
      this.newProject.name = ""
      this.modal = false;
    },
    async search() {
      if (this.searchQuery !== "") {
        let response = await ProjectService.searchProject(this.searchQuery)
        if (response.status === 200) {
          this.projects = response.data
        }
      } else {
        let response = await ProjectService.getListProjects()
        if (response.status === 200) {
          this.projects = response.data
        }
      }
    },
    async getProjects() {
      let response = await ProjectService.getListProjects()
      if (response?.status === 200) {
        this.projects = response.data
      }
    }
  },
  async mounted() {
    if (!this.currentUser) {
      this.$router.push('/login');
    }
    await this.getProjects()
  },
};
</script>
