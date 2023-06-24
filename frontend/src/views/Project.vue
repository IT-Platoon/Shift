<template>
  <div class="d-flex">
      <div class="col-8 my-3 mx-2">
        <div class="py-3 px-4 project-body bgc d-flex justify-content-between">
          <h5 class="mt-2">{{ this.project?.name }}</h5>
          <div class="dropdown">
            <button class="btn bgc" type="button" data-bs-toggle="dropdown" aria-expanded="false">
              <i class="bi bi-three-dots"></i>
            </button>
            <ul class="dropdown-menu">
              <li>
                <a
                  v-if="!this.isOwner"
                  class="dropdown-item item"
                  @click="this.leaveFromProject"
                >
                  Выйти с проекта
                </a>
              </li>
              <li>
                <a
                  v-if="this.isOwner"
                  class="dropdown-item item"
                  @click="this.changeModal"
                >
                  Редактировать проект
                </a>
              </li>
              <li>
                <a
                  v-if="this.isOwner"
                  class="dropdown-item item"
                  @click="this.removeProject"
                >
                  Удалить проект
                </a>
              </li>
            </ul>
          </div>
        </div>
        <div class="mt-2 py-2 px-4 project-body bgc">
          <div class="my-4">
            <ListResponses
              :responses="this.modelResponses"
              @createModelProcess="this.createModelProcess"
            />
          </div>
        </div>
      </div>
      <div class="col-4 my-3">
          <div class="py-4 px-4 project-body bgc">
            <ListUsersMember
              :members="this.members"
              :isOwner="this.isOwner"
              :ownerId="this.ownerId"
              @emitRemoveMember="removeMember"
            />
          </div>
          <div v-if="this.isOwner" class="my-2">
            <div class="py-4 px-4 project-body bgc">
              <ListUsersWantToEnter
                :wantToEnterUsers="this.wantToEnter"
                @emitAddMember="this.addMember"
                @emitRemoveWantToEnter="this.removeWantToEnter"
              />
            </div>
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
      } else if (response.status === 400 || response.status === 403) {
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
    async removeWantToEnter(userId) {
      console.log(userId)
      let data = {
          "user": userId,
          "project": this.id,
          "action": "REMOVE_WANT_ENTER",
      }
      let response = await ProjectService.removeWantToEnter(data)
      if (response.status === 200) {
        this.wantToEnter = response.data.want_to_enter
      } else if (response.status === 400 || response.status === 403) {
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
    async removeMember(memberId) {
      let data = {
          "user": memberId,
          "project": this.id,
          "action": "REMOVE",
      }
      let response = await ProjectService.removeMemberFromProject(data)
      if (response.status === 200) {
        this.members = response.data.members
      } else if (response.status === 400 || response.status === 403) {
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
    async leaveFromProject() {
      let response = await ProjectService.leaveFromProject(this.id)
      if (response.status === 200) {
        this.$router.push("/")
        this.$toast.open({
          message: response.data.message,
          type: "success",
          duration: 5000,
        });
      } else if (response.status === 400 || response.status === 403) {
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
    async removeProject() {
      let response = await ProjectService.removeProject(this.id)
      if (response.status === 204) {
        this.$router.push("/")
        this.$toast.open({
          message: "Вы успешно удалили проект",
          type: "success",
          duration: 5000,
        });
      } else if (response.status === 400 || response.status === 403) {
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
    changeModal() {
      this.modal = !this.modal;
    },
    async changeProject(project) {
      let response = await ProjectService.updateProject(this.id, project)
      if (response.status === 200) {
        this.modal = false;
        this.project = response.data;
      } else if (response.status === 400 || response.status === 403) {
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

<style scoped>

.bgc {
  background-color: #ced4da;
}

.project-body {
  border-radius: 10px;
}

.item {
  cursor: pointer;
}
</style>