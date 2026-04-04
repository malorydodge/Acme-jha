<template>
  <div>
    <h1 class="title">{{ isEdit ? "Edit JHA" : "Create JHA" }}</h1>

    <!-- Basic Info -->
    <div class="field">
      <label class="label">Title</label>
      <input class="input" v-model="form.title" />
      <p v-if="errors.title" class="help is-danger">{{ errors.title }}</p>
    </div>

    <div class="field">
      <label class="label">Author</label>
      <input class="input" v-model="form.author" />
      <p v-if="errors.author" class="help is-danger">{{ errors.author }}</p>
    </div>

    <div class="field">
      <label class="label">Department</label>
      <input class="input" v-model="form.department" />
      <p v-if="errors.department" class="help is-danger">
        {{ errors.department }}
      </p>
    </div>

    <!-- Steps -->
    <div class="steps">
      <div class="level">
        <h2 class="subtitle">Steps</h2>
        <button class="button is-small is-primary" @click="addStep">
          Add Step
        </button>
      </div>

      <draggable v-model="form.steps" item-key="id" handle=".drag-handle">
        <template #item="{ element: step, index }">
          <div class="box step">
            <div class="level">
              <div class="level-left">
                <span class="drag-handle" style="cursor: grab">☰</span>
                <strong>Step {{ index + 1 }}</strong>
              </div>

              <div>
                <button
                  class="button is-small"
                  @click="step.collapsed = !step.collapsed"
                >
                  {{ step.collapsed ? "Expand" : "Collapse" }}
                </button>

                <button
                  class="button is-danger is-small"
                  @click="removeStep(index)"
                >
                  Remove
                </button>
              </div>
            </div>

            <div v-if="!step.collapsed">
              <div class="field">
                <label class="label">Step Description</label>
                <input class="input" v-model="step.description" />
              </div>

              <div class="field">
                <label class="label">Photo</label>
                <input type="file" @change="onFileChange($event, step)" />

                <img
                  v-if="step.preview"
                  :src="step.preview"
                  class="step-image"
                />
              </div>

              <!-- Hazards -->
              <div class="hazards">
                <div class="level">
                  <h4 class="subtitle is-6">Hazards</h4>
                  <button class="button is-small" @click="addHazard(step)">
                    Add Hazard
                  </button>
                </div>

                <div
                  v-for="(hazard, hIndex) in step.hazards"
                  :key="hazard.id"
                  class="box hazard"
                >
                  <div class="level">
                    <strong>Hazard {{ hIndex + 1 }}</strong>

                    <div>
                      <button
                        class="button is-small"
                        @click="hazard.collapsed = !hazard.collapsed"
                      >
                        {{ hazard.collapsed ? "Expand" : "Collapse" }}
                      </button>

                      <button
                        class="button is-danger is-small"
                        @click="removeHazard(step, hIndex)"
                      >
                        Remove
                      </button>
                    </div>
                  </div>

                  <div v-if="!hazard.collapsed">
                    <div class="field">
                      <input
                        class="input"
                        placeholder="Hazard description"
                        v-model="hazard.description"
                      />
                    </div>

                    <!-- Controls -->
                    <div class="controls">
                      <div class="level">
                        <h5 class="subtitle is-7">Controls</h5>
                        <button
                          class="button is-small"
                          @click="addControl(hazard)"
                        >
                          Add Control
                        </button>
                      </div>

                      <div
                        v-for="(control, cIndex) in hazard.controls"
                        :key="control.id"
                        class="box control"
                      >
                        <div class="level">
                          <strong>Control {{ cIndex + 1 }}</strong>

                          <div>
                            <button
                              class="button is-small"
                              @click="control.collapsed = !control.collapsed"
                            >
                              {{ control.collapsed ? "Expand" : "Collapse" }}
                            </button>

                            <button
                              class="button is-danger is-small"
                              @click="removeControl(hazard, cIndex)"
                            >
                              Remove
                            </button>
                          </div>
                        </div>

                        <div v-if="!control.collapsed">
                          <input
                            class="input"
                            placeholder="Control"
                            v-model="control.description"
                          />
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </template>
      </draggable>
    </div>

    <button class="button is-primary" @click="save">
      {{ isEdit ? "Update" : "Create" }}
    </button>

    <button v-if="isEdit" class="button is-danger mx-2" @click="deleteJha">
      Delete
    </button>
    <button v-if="isEdit" class="button mx-2" @click="cancel">Cancel</button>
  </div>
</template>

<script setup>
import { reactive, onMounted, computed, watch } from "vue";
import draggable from "vuedraggable";
import { useRouter } from "vue-router";
import api from "../services/api";

const props = defineProps({
  id: {
    type: String,
    required: false,
  },
});

const router = useRouter();
const isEdit = computed(() => !!props.id);

onMounted(async () => {
  if (props.id) {
    const response = await api.get(`/jhas/${props.id}`);
    form.value = response.data;
  }
});

const cancel = () => {
  router.push("/");
};

const deleteJha = async (jha) => {
  if (confirm(`Are you sure you want to delete JHA with title ${jha.title}?`)) {
    try {
      const response = await api.delete(`/jhas/${jha.id}`);
      if (response.status === 204) {
        router.push("/");
      }
    } catch (error) {
      console.error("Error deleting item:", error);
    }
  }
};

const createStep = () => ({
  id: Date.now() + Math.random(),
  description: "",
  file: null,
  preview: null,
  collapsed: false,
  hazards: [],
});

const createHazard = () => ({
  id: Date.now() + Math.random(),
  description: "",
  collapsed: false,
  controls: [],
});

const createControl = () => ({
  id: Date.now() + Math.random(),
  description: "",
  collapsed: false,
});

const form = reactive({
  title: "",
  author: "",
  department: "",
  steps: [],
});

const errors = reactive({
  title: "",
  author: "",
  department: "",
});

watch(
  () => props.jha,
  (jha) => {
    if (jha) {
      Object.assign(form, jha);
    }
  },
  { immediate: true },
);

const validate = () => {
  errors.title = !form.title ? "Title is required" : "";
  errors.author = !form.author ? "Author is required" : "";
  errors.department = !form.department ? "Department is required" : "";

  return !errors.title && !errors.author && !errors.department;
};

const addStep = () => form.steps.push(createStep());
const removeStep = (i) => form.steps.splice(i, 1);

const addHazard = (step) => step.hazards.push(createHazard());
const removeHazard = (step, i) => step.hazards.splice(i, 1);

const addControl = (hazard) => hazard.controls.push(createControl());
const removeControl = (hazard, i) => hazard.controls.splice(i, 1);

const onFileChange = (event, step) => {
  const file = event.target.files[0];
  if (!file) return;

  step.file = file;
  step.preview = URL.createObjectURL(file);
};

const save = async () => {
  if (!validate()) return;

  const formData = new FormData();

  formData.append("title", form.title);
  formData.append("author", form.author);
  formData.append("department", form.department);

  form.steps.forEach((step, i) => {
    formData.append(`steps[${i}][description]`, step.description);

    if (step.file) {
      formData.append(`steps[${i}][photo]`, step.file);
    }

    step.hazards.forEach((hazard, h) => {
      formData.append(
        `steps[${i}][hazards][${h}][description]`,
        hazard.description,
      );

      hazard.controls.forEach((control, c) => {
        formData.append(
          `steps[${i}][hazards][${h}][controls][${c}]`,
          control.description,
        );
      });
    });
  });

  if (isEdit.value) {
    await api.put(`/jhas/${props.jha.id}`, formData);
  } else {
    await api.post("/jhas", formData);
  }

  router.push("/");
};
</script>
