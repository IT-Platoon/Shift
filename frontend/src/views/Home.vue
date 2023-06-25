<template>
  <div class="container py-2 px-4 mt-3">
      <div class="bgc radius py-3 px-4">
        <div class="input-group my-3">
          <input
            type="text"
            class="form-control search"
            placeholder="Введите название проекта для поиска"
            @input="e => this.search(e.target.value)"
          >
        </div>
        <div>
          <button
            @click="this.openModal"
            class="btn btn-dark bg-black"
          >
            Создать проект
          </button>
        </div>
      </div>
      <div class="my-3 bgc radius py-3 px-4">
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
        this.newProject.name = ""
        this.modal = false;
      } else if (response.status === 400) {
        for (const [key, value] of Object.entries(response.data)) {
          for (const item of value) {
            this.$toast.open({
              message: item,
              type: "error",
              duration: 10000,
            });
          }
        }
      }
    },
    async search(searchQuery) {
      if (searchQuery !== "") {
        let response = await ProjectService.searchProject(searchQuery)
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

<style scoped>
.bgc {
  background-color: var(--bs-gray-400);
}

.radius {
  border-radius: 10px !important;
}
</style>