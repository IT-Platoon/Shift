<template>
  <div v-if="this.projects.length">
    <ProjectItem
        v-for="project of this.projects"
        :key="project.id"
        :project="project"
    />
  </div>
  <div v-else>
    <h6>Ничего не найдено</h6>
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