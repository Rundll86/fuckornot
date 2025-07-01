<template>
    <a target="_blank" :href="href" @mouseover="mouseIn = true" @mouseleave="mouseIn = false">
        <SuspensionPrompt v-if="useSlots().prompt" :x="mouse[0]" :y="mouse[1]" :show="mouseIn">
            <slot name="prompt"></slot>
        </SuspensionPrompt>
        <slot></slot>
    </a>
</template>
<script setup lang="ts">
import { ref, useSlots } from "vue";
import SuspensionPrompt from "./SuspensionPrompt.vue";
defineProps({ href: String, unimportant: Boolean });
const mouseIn = ref(false);
const mouse = ref([0, 0]);
window.addEventListener("mousemove", (e) => {
    mouse.value = [e.clientX, e.clientY];
});
</script>
<style scoped>
a {
    transition: none;
    display: inline-block;
    text-wrap: nowrap;
}

a:link,
a:visited {
    color: black;
    text-decoration: none;
}

a:hover {
    color: gray;
    text-decoration: underline;
}

a:active {
    color: black;
    text-decoration: underline;
}
</style>