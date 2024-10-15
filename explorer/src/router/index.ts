import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router";
import MainScreen from "../components/MainScreen.vue";
import OracleDetails from "../components/OracleDetails.vue";

const routes: Array<RouteRecordRaw> = [
  {
    path: "/",
    name: "Home",
    component: MainScreen,
  },
  {
    path: "/oracle/:address",
    name: "OracleDetails",
    component: OracleDetails,
    props: true,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
