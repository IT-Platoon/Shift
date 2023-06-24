<template>
    <div class="simple-modal">
      <div class="simple-modal-backdrop" @click="this.closeModal">
        <div class="simple-modal-container">
          <div class="simple-modal-content" @click.stop>
            <header class="simple-modal-header">
                <h5 class="modal-title">{{modalName}}</h5>
            </header>
            <section class="simple-modal-body">
                <div class="mb-3">
                    <label class="col-form-label">Название</label>
                    <input type="text" v-model="project.name" class="form-control">
                </div>
            </section>
            <footer class="simple-modal-footer">
              <div class="d-flex justify-content-between">
                <button
                    @click="$emit('changeProject', project)"
                    class="btn btn-primary"
                >
                    {{buttonLabel}}
                </button>
                <button
                  class="btn btn-danger"
                  type="button"
                  @click="this.closeModal"
                >
                  Закрыть
                </button>
              </div>
            </footer>
          </div>
        </div>
      </div>
    </div>
</template>

<script>
export default {
    name: "ProjectModal",
    props: {
        show: {
            type: Boolean,
            required: true,
        },
        project: {
            type: Object,
            required: true,
        },
        modalName: {
            type: String,
            required: true,
        },
        buttonLabel: {
            type: String,
            required: true,
        },
    },
    emits: [
        "changeProject",
        "close",
    ],
    mounted() {
        window.addEventListener("keydown", this.escCloseModal);
    },
    destroy() {
        window.removeEventListener("keydown", this.escCloseModal);
    },
    methods: {
        closeModal() {
            this.$emit("close");
        },
        escCloseModal(e) {
            if (this.show && e.key === "Escape") {
                this.closeModal();
            }
        },
    },
};
</script>

<style>
.simple-modal-backdrop {
    position: fixed;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.8);
    transition: opacity 0.3s ease;
    z-index: 9999;
}

.simple-modal-container {
    position: fixed;
    top: 0;
    right: 0;
    left: 0;
    bottom: 0;
    width: auto;
    margin: 16px;
}

.simple-modal-content {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    width: 100%;
    max-width: 500px;
    margin: 1.75rem auto;
    padding: 20px 30px;
    border-radius: 5px;
    color: #000;
    background-color: #fff;
    transform: translate(0, 0);
    transition: all 0.3s ease;
    box-sizing: border-box;
}

.simple-modal-header {
    padding-bottom: 16px;
    font-size: 25px;
    text-align: center;
}

.simple-modal-footer {
    display: flex;
    flex-direction: column;
    justify-content: center;
    height: 80px;
    text-align: center;
}
</style>
