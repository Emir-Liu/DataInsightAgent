

<template>
  <h1>搜索引擎问答</h1>
  

  <div>
    <br />
      <a-input-search
        v-model:value="input_value"
        placeholder="输入你想查询的内容"
        :loading="loading_status"
        :disabled="loading_status"
        enter-button="Search"
        @search="search"
      />
  </div>

  <br>
  <br>
  <div>
    分析内容:
    <br>
    <div v-html="compiledMarkdownContent"></div>
  </div>
</template>


<script lang="ts" setup>


import { computed, ref, watchEffect } from 'vue';
import { marked } from 'marked';

import api_request from '../utils/api';

const ip = import.meta.env.VITE_BACKEND_IP
const port = import.meta.env.VITE_BACKEND_PORT
const input_value = ref<string>('');
let loading_status = ref(false)

let response = ref('')


// 清空数据内容
function clear_info() {
  response.value = ''
}

function search(e:Event){
  console.log('点击回车',e)
  console.log('input_value:', input_value.value)
  loading_status.value = true

  clear_info()

  const eventSource = new EventSource(`http://${ip}:${port}/search_engine_qa?content=${input_value.value}`);
  eventSource.onmessage = (event) => {
    const input_js = JSON.parse(event.data)
    console.log('input_js:',input_js)
    if (input_js.type == 'response_part') {
      response.value += input_js.value
    } else if (input_js.type == 'process') {
      response.value += input_js.value
    } else {
      console.log('出现未知内容')
    }
  };
  eventSource.onerror = (error) => {
      // eventData.value = ''
      // console.error('SSE error:', error);
      loading_status.value = false
      console.log('意外结束')
      eventSource.close();
  };
}


const compiledMarkdownContent = computed(() => {
    return marked(response.value)
  }
)
</script>
  
  
  
<style scoped>
</style>
  