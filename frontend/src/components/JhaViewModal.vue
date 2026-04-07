<template>
  <div class="modal" :class="{ 'is-active': isOpen }">
    <div class="modal-background" @click="close"></div>

    <div class="modal-card">
      <header class="modal-card-head">
        <p class="modal-card-title">
          {{ jha?.title || "JHA Details" }}
        </p>
        <button class="delete" @click="close"></button>
      </header>

      <section class="modal-card-body" v-if="jha">
        <div class="content">
          <div class="columns">
            <div class="column is-half">
              <p><strong>Title:</strong> {{ jha.title }}</p>
              <p><strong>Author:</strong> {{ jha.author }}</p>
              <p><strong>Department:</strong> {{ jha.department }}</p>
              <p><strong>Location:</strong> {{ jha.location || "-" }}</p>
            </div>
            <div class="column is-half">
              <p><strong>Job Title:</strong> {{ jha.job_title || "-" }}</p>
              <p><strong>Supervisor:</strong> {{ jha.supervisor || "-" }}</p>
              <p><strong>Date:</strong> {{ formatDate(jha.job_date) }}</p>
            </div>
          </div>
          <hr />

          <h4 class="title is-5">Steps</h4>

          <div
            v-if="!jha.steps || jha.steps.length === 0"
            class="notification is-light"
          >
            No steps yet
          </div>

          <div v-for="(step, sIndex) in jha.steps" :key="step.id" class="box">
            <div class="level">
              <strong>Step {{ sIndex + 1 }}</strong>

              <button
                v-if="isExpandable(step)"
                class="button is-small"
                @click="step.expanded = !step.expanded"
              >
                {{ step.expanded ? "Collapse" : "Expand" }}
              </button>
            </div>

            <div v-if="step.expanded">
              <p>{{ step.description }}</p>

              <img
                v-if="step.photo"
                :src="getPhotoUrl(step.photo)"
                class="step-image"
              />

              <!-- Hazards -->
              <div v-if="step.hazards?.length">
                <h5 class="title is-6">Hazards</h5>

                <div
                  v-for="(hazard, hIndex) in step.hazards"
                  :key="hazard.id"
                  class="box"
                >
                  <strong>Hazard {{ hIndex + 1 }}</strong>
                  <p>{{ hazard.description }}</p>

                  <div v-if="hazard.controls?.length">
                    <h6 class="title is-7">Controls</h6>

                    <div
                      v-for="control in hazard.controls"
                      :key="control.id"
                      class="box"
                    >
                      {{ control.description }}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <footer class="modal-card-foot">
        <button class="button is-primary" @click="editJha">Edit</button>
        <button class="button is-danger mx-2" @click="deleteJha">Delete</button>
        <button class="button" @click="close">Close</button>
      </footer>
    </div>
  </div>
</template>

<script setup>
import { watch } from "vue";
import api from "../services/api";

const props = defineProps({
  jha: Object,
  isOpen: Boolean,
});

const emit = defineEmits(["close", "edit", "delete"]);

const close = () => emit("close");
const editJha = () => emit("edit");
const deleteJha = () => emit("delete");

const getPhotoUrl = (photo) =>
  photo
    ? `${api.defaults.baseURL}${photo.startsWith("/") ? "" : "/"}${photo}`
    : null;

const isExpandable = (step) => {
  return (
    step.photo ||
    step.hazards?.length ||
    step.hazards?.some((h) => h.controls?.length)
  );
};

const formatDate = (date) => {
  if (!date) return "-";
  return new Date(date).toLocaleDateString();
};

watch(
  () => props.jha,
  (jha) => {
    jha?.steps?.forEach((step) => {
      step.expanded = false;
    });
  },
  { immediate: true },
);
</script>

<style scoped>
.step-image {
  margin-top: 10px;
  max-width: 400px;
  border-radius: 6px;
}
</style>
