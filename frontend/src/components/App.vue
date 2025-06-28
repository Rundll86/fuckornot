<template>
    <div class="fuckornot">
        <Navbar />
        <ContainerFrame title="配置">
            上传一张照片，让AI来评价图中角色的可操性。
            <img class="preview" :src="imageUrl" alt="Uploaded Image" v-if="imageUrl" />
            <button @click="upload">点击上传</button>
            使用的AI人格：
            <SelectBar :options="usableSouls" v-model:selected="useSoul" />
        </ContainerFrame>
        <ContainerFrame v-if="imageUrl">
            AI瞎评的，别当真！尽量别直接上传自己照片。
            <button @click="start">开始评价</button>
            <textarea disabled></textarea>
        </ContainerFrame>
    </div>
</template>
<script setup lang="ts">
import { computed, ref } from "vue";
import ContainerFrame from "./ContainerFrame.vue";
import Navbar from "./Navbar.vue";
import SelectBar from "./SelectBar.vue";
const imageFile = ref<File | null>(null);
const imageData = ref<ArrayBuffer | null>(null);
const imageUrl = computed(() => {
    if (!imageData.value) return "";
    try {
        URL.revokeObjectURL(imageUrl.value);
    } catch (e) {
        console.error("Error revoking object URL:", e);
    }
    return URL.createObjectURL(new Blob([imageData.value]));
});
const useSoul = ref(0);
const usableSouls = [
    "欲望化身",
    "霸道总裁",
    "耽美鉴赏家",
    "恋物诗人",
    "纯欲神官",
    "百合诗人",
];
function upload() {
    const input = document.createElement("input");
    input.type = "file";
    input.accept = "image/*";
    input.onchange = () => {
        const file = input.files?.[0];
        if (file) {
            imageFile.value = file;
            const reader = new FileReader();
            reader.onload = () => {
                imageData.value = reader.result as ArrayBuffer;
            };
            reader.readAsArrayBuffer(file);
        }
    };
    input.click();
}
async function start() {
    if (!imageFile.value) return;
    const form = new FormData();
    form.append("image", imageFile.value);
    form.append("soul", usableSouls[useSoul.value]);
    const response = await fetch("/api", {
        method: "POST",
        body: form
    }).then(e => e.json());
    console.log(response);
}
</script>
<style scoped>
.fuckornot {
    padding: 80px;
}

.preview {
    width: 50vw;
    border: 2px solid gray;
}

button {
    border: 2px solid gray;
    padding: 5px 10px;
    border-radius: 5px;
}

button:hover {
    border-color: rgb(68, 68, 68);
    cursor: pointer;
}

input,
textarea {
    border: gray 2px solid;
    transition: none;
}
</style>