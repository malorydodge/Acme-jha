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
      <div class="level" v-if="form.steps.length || isAddingStep">
        <h2 class="subtitle">Steps</h2>
        <button class="button is-small is-primary" @click="addStep">
          Add Step
        </button>
      </div>
      <p v-else>No steps yet</p>

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
                  class="button is-small mx-1"
                  @click="step.collapsed = !step.collapsed"
                >
                  {{ step.collapsed ? "Expand" : "Collapse" }}
                </button>

                <button
                  class="button is-danger is-small mx-1"
                  @click="removeStep(index)"
                >
                  Remove
                </button>
              </div>
            </div>

            <div v-if="!step.collapsed">
              <!-- Step Description -->
              <div class="field">
                <label class="label">Step Description</label>
                <input class="input" v-model="step.description" />
              </div>

              <!-- Photo -->
              <div class="field">
                <label class="label">Photo</label>
                <input
                  type="file"
                  @change="onFileChange($event, step)"
                  :value="step.file?.name || ''"
                />

                <div v-if="step.preview || step.photo">
                  <img
                    :src="step.preview || getPhotoUrl(step.photo)"
                    class="step-image"
                  />
                  <button
                    class="button is-small is-danger mt-1 is-pulled-right"
                    @click="removePhoto(step)"
                  >
                    Remove Photo
                  </button>
                  <p>{{ step.file?.name || getFileName(step.photo) }}</p>
                </div>
              </div>

              <!-- Hazards -->
              <div
                class="hazards"
                v-if="step.hazards.length || step.isAddingHazard"
              >
                <div class="level">
                  <h4 class="subtitle is-4">Hazards</h4>
                  <button class="button is-small mx-1" @click="addHazard(step)">
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
                        class="button is-small mx-1"
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
                    <div
                      class="controls"
                      v-if="hazard.controls.length || hazard.isAddingControl"
                    >
                      <div class="level">
                        <h5 class="subtitle is-5">Controls</h5>
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
                              class="button is-small mx-1"
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
                    <p v-else class="has-text-grey">No controls yet</p>
                  </div>
                </div>
              </div>
              <p v-else class="has-text-grey">No hazards yet</p>
            </div>
          </div>
        </template>
      </draggable>
    </div>
    <div class="container m-2">
      <button v-if="isEdit" class="button is-pulled-right mr-2" @click="cancel">
        Cancel
      </button>

      <button
        v-if="isEdit"
        class="button is-danger mx-2 is-pulled-right"
        @click="deleteJha"
      >
        Delete
      </button>

      <button class="button is-primary is-pulled-right" @click="save">
        {{ isEdit ? "Update" : "Create" }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { reactive, onMounted, computed } from "vue";
import draggable from "vuedraggable";
import { useRouter } from "vue-router";
import api from "../services/api";

const props = defineProps({ id: String });
const router = useRouter();
const isEdit = computed(() => !!props.id);

// Step / Hazard / Control Factories
const createStep = () => ({
  id: Date.now() + Math.random(),
  description: "",
  file: null,
  preview: null,
  photo: null,
  collapsed: false,
  hazards: [],
  isAddingHazard: false,
});

const createHazard = () => ({
  id: Date.now() + Math.random(),
  description: "",
  collapsed: false,
  controls: [],
  isAddingControl: false,
});

const createControl = () => ({
  id: Date.now() + Math.random(),
  description: "",
  collapsed: false,
});

// Reactive form state
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

// Helpers for photos
const getPhotoUrl = (photo) =>
  photo ? `http://localhost:8000/${photo}` : null;
const getFileName = (photo) => photo?.split("/").pop() || "";

// Lifecycle
onMounted(async () => {
  if (props.id) {
    const response = await api.get(`/jhas/${props.id}`);
    Object.assign(form, response.data);

    form.steps.forEach((step) => {
      step.collapsed = false;
      step.isAddingHazard = step.hazards?.length > 0;
      step.hazards?.forEach((hazard) => {
        hazard.collapsed = false;
        hazard.isAddingControl = hazard.controls?.length > 0;
      });
    });
  }
});

// Actions
const cancel = () => router.push("/");
const deleteJha = async () => {
  if (confirm("Delete this JHA?")) {
    await api.delete(`/jhas/${props.id}`);
    router.push("/");
  }
};
const validate = () => {
  errors.title = !form.title ? "Title is required" : "";
  errors.author = !form.author ? "Author is required" : "";
  errors.department = !form.department ? "Department is required" : "";
  return !errors.title && !errors.author && !errors.department;
};

// Add / Remove
const addStep = () => {
  const step = createStep();
  step.isAddingHazard = true;
  form.steps.push(step);
};
const removeStep = (i) => form.steps.splice(i, 1);

const addHazard = (step) => {
  const hazard = createHazard();
  hazard.isAddingControl = true;
  step.hazards.push(hazard);
  step.isAddingHazard = true;
};
const removeHazard = (step, i) => {
  step.hazards.splice(i, 1);
  if (!step.hazards.length) step.isAddingHazard = false;
};

const addControl = (hazard) => {
  hazard.controls.push(createControl());
  hazard.isAddingControl = true;
};
const removeControl = (hazard, i) => {
  hazard.controls.splice(i, 1);
  if (!hazard.controls.length) hazard.isAddingControl = false;
};

// File handling
const onFileChange = (event, step) => {
  const file = event.target.files[0];
  if (!file) return;
  step.file = file;
  step.preview = URL.createObjectURL(file);
};

const removePhoto = (step) => {
  step.file = null;
  step.preview = null;
  step.photo = null;
};

// Save
const save = async () => {
  if (!validate()) return;

  const formData = new FormData();
  formData.append("title", form.title);
  formData.append("author", form.author);
  formData.append("department", form.department);

  formData.append(
    "steps",
    JSON.stringify(
      form.steps.map((step) => ({
        description: step.description,
        photo: step.photo,
        hazards: step.hazards.map((hazard) => ({
          description: hazard.description,
          controls: hazard.controls.map((control) => ({
            description: control.description,
          })),
        })),
      })),
    ),
  );

  form.steps.forEach((step) => {
    if (step.file) formData.append("photos", step.file);
  });

  if (isEdit.value) {
    await api.put(`/jhas/${props.id}`, formData);
  } else {
    await api.post("/jhas", formData);
  }

  router.push("/");
};
</script>

<style scoped>
.step-image {
  margin-top: 10px;
  max-width: 400px;
  border-radius: 6px;
}
</style>
