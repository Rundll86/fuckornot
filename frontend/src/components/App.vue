<template>
    <div class="fuckornot">
        <NavLine />
        <ContainerFrame title="配置">
            上传一张照片，让AI来评价图中角色的可操性。
            <img class="preview" :src="imageUrl" alt="Uploaded Image" v-if="imageUrl" />
            <button @click="upload">点击上传</button>
            回复语言：
            <SelectBar :options="languages" v-model:selected="language" />
            使用的AI人格：
            <SelectBar :options="soulsKeyMap" v-model:selected="useSoul" />
            <div class="output" @click="checkPreview">
                {{ previewing ? soulsKeyPair[soulsKeyMap[useSoul]] : "点击展示提示词" }}
            </div>
        </ContainerFrame>
        <ContainerFrame title="输出" v-if="imageUrl">
            AI瞎评的，别当真！尽量别直接上传自己照片。
            <button :disabled="loading" @click="start">
                {{ error ? "发生错误，请刷新网页重试" : loading ? "AI回复中" : "开始评价" }}
            </button><br>
            <span v-if="rate >= 0">可操性：{{ rate }}/10，{{ verdict ? "上了😍" : "不上🤮" }}</span>
            <span v-if="appe >= 0">颜值评分：{{ appe }}/10</span>
            <div class="output">{{ aiOutput }}</div>
        </ContainerFrame>
        <FootBar />
    </div>
</template>
<script setup lang="ts">
import { computed, ref } from "vue";
import ContainerFrame from "./ContainerFrame.vue";
import NavLine from "./NavLine.vue";
import SelectBar from "./SelectBar.vue";
import FootBar from "./FootBar.vue";

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
const loading = ref(false);
const error = ref(false);
const previewing = ref(false);

const useSoul = ref(0);

const aiOutput = ref("");
const rate = ref(-1);
const verdict = ref(false);
const appe = ref(-1);
const language = ref(0);

const languages = ["中文", "English", "日本語", "한국어"];
const contextRequire = require.context("../../../public/prompts", false, /\.txt$/i);
const soulsKeyMap = ref(contextRequire.keys().map(removeSuffixAndPrefix).sort((a, b) => {
    if (a.startsWith("⚠️") && !b.startsWith("⚠️")) return 1;
    if (!a.startsWith("⚠️") && b.startsWith("⚠️")) return -1;
    return 0;
}));
const soulsKeyPair = ref(Object.fromEntries(soulsKeyMap.value.map(key => [key, contextRequire(`./${key}.txt`).default])));

function removeSuffixAndPrefix(target: string) {
    return target.slice(2, -4);
}
function base64ToBuffer(base64: string): ArrayBuffer {
    const binaryString = atob(base64.split(',')[1]);
    const len = binaryString.length;
    const bytes = new Uint8Array(len);
    for (let i = 0; i < len; i++) {
        bytes[i] = binaryString.charCodeAt(i);
    }
    return bytes.buffer;
}

function checkPreview() {
    previewing.value = !previewing.value;
}
function upload() {
    const input = document.createElement("input");
    input.type = "file";
    input.accept = "image/*";
    input.onchange = async () => {
        const file = input.files?.[0];
        if (file) {
            imageFile.value = file;
            const reader = new FileReader();
            reader.addEventListener("load", () => {
                imageData.value = reader.result as ArrayBuffer;
            });
            reader.addEventListener("error", (e) => {
                console.error("FileReader error:", e);
                uploadAsBase64(file);
            });
            try {
                reader.readAsArrayBuffer(file);
            } catch (e) {
                console.error("Error reading file:", e);
                uploadAsBase64(file);
            }
        }
    };
    input.click();
}
async function uploadAsBase64(file: File) {
    const reader = new FileReader();
    return new Promise((resolve) => {
        reader.onload = () => {
            const base64Data = reader.result as string;
            imageData.value = base64ToBuffer(base64Data);
            resolve(base64Data);
        };
        reader.readAsDataURL(file);
    });
}
async function start() {
    loading.value = true;
    if (!imageFile.value) return;
    const form = new FormData();
    if (imageData.value) {
        form.append("image", imageFile.value);
    } else if (imageUrl.value.startsWith("data:")) {
        form.append("image", imageUrl.value);
    }
    form.append("soul", soulsKeyMap.value[useSoul.value]);
    form.append("language", languages[language.value]);
    try {
        const response = JSON.parse(await fetch("/api", {
            method: "POST",
            body: form
        }).then(e => e.text()));
        console.log(response);
        aiOutput.value = response.explanation;
        rate.value = response.rating;
        verdict.value = response.verdict;
        appe.value = response.appearance;
    } catch (e) {
        error.value = true;
    } finally {
        loading.value = false;
    }
}
</script>
<style scoped>
.fuckornot {
    padding: 80px 0;
    display: flex;
    flex-direction: column;
    align-items: center;
}

.preview {
    width: 300px;
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
    padding: 3px 5px;
    border-radius: 5px;
}

.output {
    max-width: 50%;
}
</style>