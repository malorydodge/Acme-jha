<template>
  <div>
    <h1 class="title">{{ isEdit ? "Edit JHA" : "Create JHA" }}</h1>

    <!-- Basic Info -->
    <div class="field">
      <label class="label">Title</label>
      <input class="input" v-model="form.title" />
      <p v-if="errors.title" class="help is-danger">{{ errors.title }}</p>
    </div>

    <div class="columns">
      <div class="column is-half">
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

        <div class="field">
          <label class="label">Location</label>
          <input class="input" v-model="form.location" />
        </div>
      </div>

      <div class="column is-half">
        <div class="field">
          <label class="label">Job Title</label>
          <input class="input" v-model="form.job_title" />
        </div>

        <div class="field">
          <label class="label">Supervisor</label>
          <input class="input" v-model="form.supervisor" />
        </div>

        <div class="field">
          <label class="label">Date</label>
          <input
            type="text"
            class="input"
            v-model="form.job_date"
            placeholder="mm/dd/yyyy"
          />
        </div>
      </div>
    </div>
    <!-- Steps -->
    <div class="steps">
      <div class="level">
        <h2 v-if="form.steps.length" class="subtitle">Steps</h2>
        <p v-else>No steps yet</p>
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
                <p v-if="step.error" class="help is-danger">
                  {{ step.error }}
                </p>
              </div>

              <!-- Step Notes -->
              <div class="field">
                <label class="label">Step Notes</label>
                <textarea class="textarea" v-model="step.notes"></textarea>
              </div>

              <!-- Step Completed -->
              <div class="field">
                <label class="label checkbox is-pulled-right"
                  >Completed:
                  <input type="checkbox" v-model="step.completed" />
                </label>
              </div>

              <!-- Photo -->
              <div class="field">
                <label class="label">Photo</label>
                <input
                  type="file"
                  @change="onFileChange($event, step)"
                  accept="image/*"
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

                  <p>
                    {{ step.file?.name || getFileName(step.photo) }}
                  </p>
                </div>
              </div>

              <!-- Hazards -->
              <div class="hazards">
                <div class="level">
                  <h4 class="subtitle is-4" v-if="step.hazards.length">
                    Hazards
                  </h4>
                  <p v-else class="has-text-grey">No hazards yet</p>
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
                      <p v-if="hazard.error" class="help is-danger">
                        {{ hazard.error }}
                      </p>
                    </div>

                    <!-- Controls -->
                    <div class="controls">
                      <div class="level">
                        <h5 class="subtitle is-5" v-if="hazard.controls.length">
                          Controls
                        </h5>
                        <p v-else class="has-text-grey">No controls yet</p>
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
                          <p v-if="control.error" class="help is-danger">
                            {{ control.error }}
                          </p>
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

// Date Helpers
const formatDateDisplay = (date) => {
  if (!date) return "";

  const [year, month, day] = date.split("T")[0].split("-");
  return `${month}/${day}/${year}`;
};

const formatForSave = (dateStr) => {
  if (!dateStr) return "";
  const [month, day, year] = dateStr.split("/");
  return month && day && year ? `${year}-${month}-${day}` : dateStr;
};

// Step / Hazard / Control Factories
const createStep = () => ({
  id: Date.now() + Math.random(),
  description: "",
  notes: "",
  completed: false,
  error: "",
  file: null,
  preview: null,
  photo: null,
  collapsed: false,
  hazards: [],
});

const createHazard = () => ({
  id: Date.now() + Math.random(),
  description: "",
  error: "",
  collapsed: false,
  controls: [],
});

const createControl = () => ({
  id: Date.now() + Math.random(),
  description: "",
  error: "",
  collapsed: false,
});

const form = reactive({
  title: "",
  author: "",
  department: "",
  location: "",
  job_title: "",
  supervisor: "",
  job_date: "",
  steps: [],
});

const errors = reactive({
  title: "",
  author: "",
  department: "",
});

// Helpers for photos
const getPhotoUrl = (photo) => {
  if (!photo) return null;

  const base = import.meta.env.VITE_API_URL.replace(/\/+$/, "");
  const path = photo.replace(/^\/+/, "");

  return `${base}/${path}`;
};

const getFileName = (photo) => photo?.split("/").pop() || "";

// Lifecycle
onMounted(async () => {
  if (props.id) {
    const response = await api.get(`/jhas/${props.id}`);
    Object.assign(form, response.data);

    form.job_date = formatDateDisplay(form.job_date);

    form.steps.forEach((step) => {
      step.collapsed = false;
      step.preview = null;
      step.hazards?.forEach((hazard) => {
        hazard.collapsed = false;
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

  let valid = !errors.title && !errors.author && !errors.department;

  form.steps.forEach((step) => {
    step.error = !step.description ? "Step description is required" : "";
    if (step.error) valid = false;

    step.hazards.forEach((hazard) => {
      hazard.error = !hazard.description
        ? "Hazard description is required"
        : "";
      if (hazard.error) valid = false;

      hazard.controls.forEach((control) => {
        control.error = !control.description
          ? "Control description is required"
          : "";
        if (control.error) valid = false;
      });
    });
  });

  return valid;
};

// Add / Remove
const addStep = () => {
  const step = createStep();
  form.steps.push(step);
};

const removeStep = (i) => form.steps.splice(i, 1);

const addHazard = (step) => {
  const hazard = createHazard();
  step.hazards.push(hazard);
};

const removeHazard = (step, i) => {
  step.hazards.splice(i, 1);
};

const addControl = (hazard) => {
  hazard.controls.push(createControl());
};

const removeControl = (hazard, i) => {
  hazard.controls.splice(i, 1);
};

// File handling
const onFileChange = (event, step) => {
  const file = event.target.files[0];
  if (!file) return;
  step.file = file;
  step.preview = URL.createObjectURL(file);
  // Clear saved photo so preview takes precedence
  step.photo = null;
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
  formData.append("location", form.location || "");
  formData.append("job_title", form.job_title || "");
  formData.append("supervisor", form.supervisor || "");
  formData.append("job_date", formatForSave(form.job_date) || "");

  formData.append(
    "steps",
    JSON.stringify(
      form.steps.map((step) => ({
        description: step.description,
        notes: step.notes,
        completed: step.completed,
        photo: step.file ? null : step.photo,
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
    if (step.file) {
      formData.append("photos", step.file);
    }
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
