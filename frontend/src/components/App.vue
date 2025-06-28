<template>
    <div class="fuckornot">
        <Navbar />
        <ContainerFrame>
            上传一张照片，让AI来评价图中角色的可操性。
        </ContainerFrame>
    </div>
</template>
<script setup lang="ts">
import ContainerFrame from './ContainerFrame.vue';
import Navbar from './Navbar.vue';
</script>
<style scoped>
.fuckornot {
    padding: 80px;
}
</style>