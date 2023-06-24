<template>
    <div class="d-flex">
        <div class="col-8 m-3">
            <p>Проект: {{ this.project?.name }}</p>
            <div class="d-flex justify-content-between">
                <button
                  v-if="!this.isOwner"
                  class="btn btn-danger"
                  @click="this.leaveFromProject"
                >
                    Выйти с проекта
                </button>
                <button
                  v-if="this.isOwner"
                  class="btn btn-secondary mx-2"
                  @click="this.changeModal"
                >
                    Редактировать проект
                </button>
                <button
                  v-if="this.isOwner"
                  class="btn btn-danger"
                  @click="this.removeProject"
                >
                    Удалить проект
                </button>
            </div>
            <div class="my-4">
                <ListResponses
                  :responses="this.modelResponses"
                  @createModelProcess="this.createModelProcess"
                />
            </div>
        </div>
        <div class="col-4 my-3">
            <ListUsersMember
                :members="this.members"
                :isOwner="this.isOwner"
                :ownerId="this.ownerId"
                @emitRemoveMember="removeMember"
            />
            <div v-if="this.isOwner" class="my-3">
                <ListUsersWantToEnter
                  :wantToEnterUsers="this.wantToEnter"
                  @emitAddMember="this.addMember"
                  @emitRemoveWantToEnter="this.removeWantToEnter"
                />
            </div>
        </div>
        <ProjectModal
          v-if="this.project !== null"
          v-show="this.modal"
          :show="this.modal"
          :project="JSON.parse(JSON.stringify(this.project))"
          :modalName="this.modalName"
          :buttonLabel="this.buttonLabel"
          @changeProject="this.changeProject"
          @close="changeModal"
        />
    </div>
</template>

<script>
import ProjectService from "../services/project.service.js";
import ModelProcessService from "../services/modelProcess.service.js";
import ListResponses from "../components/ListResponses.vue";
import ListUsersMember from "../components/ListUsersMember.vue";
import ListUsersWantToEnter from "../components/ListUsersWantToEnter.vue";
import ProjectModal from "../components/ProjectModal.vue";

export default {
  name: "Project",
  components: {
    ListResponses,
    ListUsersMember,
    ListUsersWantToEnter,
    ProjectModal,
  },
  data() {
    return {
      id: this.$route.params.projectId,
      members: [],
      wantToEnter: [],
      modelResponses: [],
      project: null,
      isOwner: false,
      ownerId: 0,
      modal: false,
      modalName: "Обновить проект",
      buttonLabel: "Обновить",
    };
  },
  computed: {
    currentUser() {
      return this.$store.state.auth.user;
    },
  },
  methods: {
    async createModelProcess(file) {
      let formData = new FormData()
      formData.append("request_file", file)
      formData.append("project", this.id)
      let response = await ModelProcessService.createModelProcess(formData)
      if (response.status === 201) {
        this.modelResponses.push(response.data.model_process)
        this.$toast.open({
          message: response.data.message,
          type: "success",
          duration: 5000,
        });
      }
    },
    async sendRequestToEnter() {
      let response = await ProjectService.postWantEnterToProject(
        this.project.id,
      )
      if (response.status === 200) {
        this.project.send_request = !this.project.send_request 
        this.$toast.open({
          message: response.data.message,
          type: "success",
          duration: 5000,
        });
      }
    },
    async sendRemoveRequestToEnter() {
      let response = await ProjectService.postRemoveRequestToProject(
        this.project.id,
      )
      if (response.status === 200) {
        this.project.send_request = !this.project.send_request;
        this.$toast.open({
          message: response.data.message,
          type: "success",
          duration: 5000,
        });
      }
    },
    async addMember(userId) {
      let data = {
          "user": userId,
          "project": this.id,
          "action": "ADD",
      }
      let response = await ProjectService.addMemberToProject(data)
      if (response.status === 200) {
        this.members = response.data.members
        this.wantToEnter = response.data.want_to_enter
      }
    },
    async removeWantToEnter(userId) {
      console.log(userId)
      let data = {
          "user": userId,
          "project": this.id,
          "action": "REMOVE_WANT_ENTER",
      }
      let response = await ProjectService.removeWantToEnter(data)
      if (response.status === 200) {
        this.wantToEnter = response.data
      }
    },
    async removeMember(memberId) {
      let data = {
          "user": memberId,
          "project": this.id,
          "action": "REMOVE",
      }
      let response = await ProjectService.removeMemberFromProject(data)
      if (response.status === 200) {
        this.members = response.data
      }
    },
    async leaveFromProject() {
      let response = await ProjectService.leaveFromProject(this.id)
      if (response.status === 200) {
        this.$router.push("/")
        this.$toast.open({
          message: response.data.message,
          type: "success",
          duration: 5000,
        });
      }
    },
    async removeProject() {
      let response = await ProjectService.removeProject(this.id)
      if (response.status === 204) {
        this.$router.push("/")
        this.$toast.open({
          message: "Вы успешно удалили проект",
          type: "success",
          duration: 5000,
        });
      }
    },
    changeModal() {
      this.modal = !this.modal;
    },
    async changeProject(project) {
      let response = await ProjectService.updateProject(this.id, project)
      if (response.status === 200) {
        this.modal = false;
        this.project = response.data;
      } else if (response.status === 400) {
        if ("non_field_errors" in response.data) {
          this.$toast.open({
            message: response.data.non_field_errors,
            type: "error",
            duration: 5000,
          });
        } else {
          this.$toast.open({
            message: response.data.name,
            type: "error",
            duration: 5000,
          });
        }
      }
    },
    async getProjectInfo() {
      let response = await ProjectService.getProjectInfo(this.id)
      if (response.status === 200) {
        this.project = response.data
      }
    },
    async getProjectMembers() {
      let response = await ProjectService.getProjectMembers(this.id)
      if (response.status === 200) {
        this.members = response.data
      }
    },
    async getModelProcesses() {
      let response = await ProjectService.getModelProcesses(this.id)
      if (response.status === 200) {
        this.modelResponses = response.data
      }
    },
    async getProjectWantToEnter() {
      let response = await ProjectService.getProjectWantToEnter(this.id)
      if (response.status === 200) {
        this.wantToEnter = response.data
      }
    },
  },
  async mounted() {
    if (!this.currentUser) {
      this.$router.push('/login');
    }
    await this.getProjectInfo()
    await this.getProjectMembers()
    await this.getModelProcesses()
    this.isOwner = this.currentUser.id === this.project.owner
    this.ownerId = this.project.owner
    if (this.isOwner) {
      await this.getProjectWantToEnter()
    }
  },
};
</script>
