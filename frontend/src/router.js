import { createRouter, createWebHistory } from "vue-router";
import JhaList from "./components/JhaList.vue";
import JhaForm from "./components/JhaForm.vue";

const routes = [
  { path: "/", component: JhaList },
  { path: "/create", name: "JhaCreate", component: JhaForm },
  {
    path: "/jhas/:id/edit",
    name: "JhaEdit",
    component: JhaForm,
    props: true,
  },
];

export default createRouter({
  history: createWebHistory(),
  routes,
});
