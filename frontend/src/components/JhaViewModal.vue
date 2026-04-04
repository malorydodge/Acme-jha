<template>
  <div class="modal" :class="{ 'is-active': isOpen }">
    <div class="modal-background" @click="close"></div>

    <div class="modal-card">
      <header class="modal-card-head">
        <p class="modal-card-title">
          {{ jha?.title || "JHA Details" }}
        </p>
        <button class="delete" aria-label="close" @click="close"></button>
      </header>

      <section class="modal-card-body" v-if="jha">
        <div class="content">
          <p><strong>Title:</strong> {{ jha.title }}</p>
          <p><strong>Author:</strong> {{ jha.author }}</p>
          <p><strong>Department:</strong> {{ jha.department }}</p>

          <hr />

          <h4 class="title is-5">Steps</h4>
          <div v-if="jha.steps?.length">
            <div v-for="step in jha.steps" :key="step.id" class="box">
              {{ step.description }}
            </div>
          </div>
          <p v-else>No steps yet</p>
        </div>
      </section>

      <footer class="modal-card-foot">
        <button class="button is-primary mr-2" @click="editJha">Edit</button>
        <button
          class="button is-danger mx-2 is-pulled-right"
          @click.stop="deleteJha(jha)"
        >
          Delete
        </button>
        <button class="button mx-2" @click="close">Close</button>
      </footer>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from "vue-router";

const props = defineProps({
  jha: Object,
  isOpen: Boolean,
});

const emit = defineEmits(["close"]);

const router = useRouter();

const close = () => {
  emit("close");
};

const editJha = () => {
  emit("edit");
};

const deleteJha = () => {
  emit("delete");
  emit("close");
};
</script>
