<template>
  <div class="container card py-2 px-4 container-list-projects scroll-area overflow-auto">
    <div class="row" v-if="this.projects.length">
      <ProjectItem
          v-for="project of this.projects"
          :key="project.id"
          :project="project"
      />
    </div>
    <div v-else>
      <h6 class="m-0">Ничего не найдено</h6>
    </div>
  </div>
</template>

<script>
import ProjectItem from "./ProjectItem.vue";

export default {
  name: "ListProjects",
  components: {
    ProjectItem,
  },
  props: {
    projects: {
      type: Array,
      required: true,
    },
  },
};
</script>

<style scoped>
.card.container-list-projects {
  background-color: var(--bs-gray-100);
}

.scroll-area {
  max-height: 600px;
}
</style>