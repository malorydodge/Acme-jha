<template>
  <div>
    <nav class="level mx-5">
      <div class="level-left">
        <div class="level-item">
          <p class="subtitle is-5">
            <strong>{{ filteredItems.length }}</strong> JHAs
          </p>
        </div>
        <div class="level-item">
          <div class="field has-addons">
            <p class="control">
              <input
                class="input"
                type="text"
                placeholder="Find a JHA"
                v-model="searchQuery"
              />
            </p>
            <p class="control">
              <button class="button">Search</button>
            </p>
          </div>
        </div>
      </div>
      <div class="level-right">
        <div class="level-item">
          <button class="button is-primary" @click="$router.push('/create')">
            Create JHA
          </button>
        </div>
      </div>
    </nav>

    <div
      class="box"
      v-for="jha in filteredItems"
      :key="jha.id"
      @click="viewJha(jha)"
      style="cursor: pointer"
    >
      {{ jha.title }}

      <button
        class="button is-danger mx-2 is-pulled-right"
        @click.stop="deleteJha(jha)"
      >
        Delete
      </button>

      <button class="button mx-2 is-pulled-right" @click.stop="editJha(jha)">
        Edit
      </button>
    </div>

    <JhaViewModal
      :jha="selectedJha"
      :isOpen="showModal"
      @close="showModal = false"
      @edit="editJha(selectedJha)"
      @delete="deleteJha(selectedJha)"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { useRouter } from "vue-router";
import api from "../services/api";
import JhaViewModal from "../components/JhaViewModal.vue";

const jhas = ref([]);
const router = useRouter();
const selectedJha = ref(null);
const showModal = ref(false);
const searchQuery = ref("");

onMounted(async () => {
  refreshData();
});

const refreshData = async () => {
  const response = await api.get("/jhas");
  jhas.value = response.data;
};

const filteredItems = computed(() => {
  return jhas.value.filter((jha) => {
    return jha.title.toLowerCase().includes(searchQuery.value.toLowerCase());
  });
});

const viewJha = (jha) => {
  selectedJha.value = jha;
  showModal.value = true;
};

const editJha = (jha) => {
  router.push({
    name: "JhaEdit",
    params: {
      id: jha.id,
    },
  });
};

const deleteJha = async (jha) => {
  if (confirm(`Are you sure you want to delete JHA with title ${jha.title}?`)) {
    try {
      const response = await api.delete(`/jhas/${jha.id}`);
      if (response.status === 204) {
        refreshData();
      }
    } catch (error) {
      console.error("Error deleting item:", error);
    }
  }
};
</script>
