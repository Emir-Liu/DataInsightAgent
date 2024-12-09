

<template>
  <h1>搜索引擎问答</h1>
  

  <div>
    <br />
      <!-- <input type="text" autofocus='true' :readonly="loading_status" v-bind:value="input_value">
      <button @click="search">Search</button> -->
      <a-input-search
        v-model:value="input_value"
        placeholder="输入你想查询的内容"
        :loading="loading_status"
        :disabled="loading_status"
        enter-button="Search"
        @change="change"
        @search="search"
      />
  </div>

  <br>
  <br>
  <div>
    大模型分析内容:
    <br>
    {{ sql_ana }}
  </div>
</template>


<script lang="ts" setup>
const ip = import.meta.env.VITE_BACKEND_IP
const port = import.meta.env.VITE_BACKEND_PORT


import { v4 as uuidv4 } from 'uuid';
import { computed, ref, watchEffect } from 'vue';
import api_request from '../utils/api';

let databaseLoadStatus = ref(false)
function connectDatabase() {
  databaseLoadStatus.value = true
  api_request.DatabaseOperator.init_database().then(() => {
    databaseLoadStatus.value = false
  })
}

const input_value = ref<string>('');
let loading_status = ref(false)

let related_tables = ref([])
let sql_ana = ref('')
let sql_cmd = ref('')
let res_status = ref('')
let res_list = ref([])

let selectScene = ref('自动')
let sceneList = ref(['a','b'])
let selectSceneRes = ref('')
let question_id = ref('')
let currentStatus = ref('')
const fullSceneList = computed(() => {
    console.log('sceneList:',sceneList)
    sceneList.value.push("自动");
    console.log('fullSceneList:',sceneList.value)
    return sceneList.value
  }
)


function updateSceneList(){
  console.log('更新使用场景')
  api_request.SceneOperator.list_scene().then(
    (params) => {
      sceneList.value = params.data.scene
    }
  )
}

updateSceneList();
// 清空数据内容
function clear_info() {

  sql_ana.value = ''
  selectSceneRes.value = ''
  sql_cmd.value = ''
  res_status.value =  ''
  res_list.value = []
}

function search(e:Event){
  console.log('点击回车',e)
  console.log('input_value:', input_value.value)
  loading_status.value = true

  clear_info()

  question_id.value = uuidv4()
  const eventSource = new EventSource(`http://${ip}:${port}/text2sql/service_create_sql_stream/?content=${input_value.value}&scene=${selectScene.value}&question_id=${question_id.value}&user_id=0230`);
  // currentStatus.value = '选择场景中。。。'
  eventSource.onmessage = (event) => {
    const input_js = JSON.parse(event.data)
    console.log('input_js:',input_js)

    if (input_js.id == question_id.value) {
      const type = input_js.type
      const value = input_js.value
      const status = input_js.status
      // scene response_part sql cmd
      if (type == 'scene') {
        // currentStatus.value = '选择场景中。。。'
        selectSceneRes.value = value
      } else if (type == 'response_part') {
        if (status == 'start') {
          // currentStatus.value = '开始生成查询语句。。。'
          sql_ana.value = ''
        } else if (status == 'ok') {
          sql_ana.value += value
        }
      } else if (type == 'sql_cmd') {
        // currentStatus.value = '开始执行查询语句'
        sql_cmd.value = value
      } else if (type == 'sql_cmd_msg' ) {
        // currentStatus.value = '查询语句执行结束'
        res_status.value = value
      } else if (type == 'res_list') {
        // currentStatus.value = '成功获取数据'
        res_list.value = value
      } else if (type == 'status') {
        if (value == 'end') {
          // currentStatus.value = '当前查询处理完成'
          loading_status.value = false
          eventSource.close()
        }
      } else if (type == 'process') {
        currentStatus.value = value
      }
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

function get_service_sql (response:any) {
  // const response_fake = {"status": 0, "msg": "service create sql success","related_tables_list":["111","222"],"sql":"sql"}
  console.log('启动服务:',response)
  related_tables.value = response.data.related_tables_list
  sql_ana.value = response.data.response
  sql_cmd.value = response.data.sql_cmd
  
  res_list.value = response.data.res_content
  res_status.value = response.data.sql_cmd_msg
  loading_status.value = false
  selectSceneRes.value = response.data.scene
  console.log('res_list:',res_list)
}

function change(e:Event){
  console.log('修改内容',e)
  console.log('tableHeaders:',tableHeaders)
  console.log('env:', import.meta.env)
  console.log('ip:',ip)
  console.log('port:',port)
  updateSceneList()
}
  
function execSQLCmd() {
  console.log('开始执行SQL指令', sql_cmd.value)
  const params = {
    'sql_cmd': sql_cmd.value
  }
  api_request.DatabaseOperator.exec_sql_cmd(params).then(get_sql_res)
}


function get_sql_res(response:any) {
  console.log('执行sql指令:', response)
  res_list.value = response.data.res_content
  res_status.value = response.data.msg
}

// 计算属性，用于获取所有字段名作为表头
const tableHeaders = computed(() => {
  const headers = [];
  console.log('res_list len:',res_list.value.length)
  if (res_list.value.length > 0) {
    const keys = Object.keys(res_list.value[0]);
    headers.push(...keys);
    console.log('headers',headers)
  }
  return headers;
});

const limitResList = computed(() => {
    const maxRows = 10
    if (res_list.value.length > maxRows) {
      return res_list.value.slice(0, maxRows);
    }
    return res_list.value
  }
)

console.log('tableHeaders:',tableHeaders)

// 监听变量的变化
watchEffect(() => {
  console.log('当前内容:', sql_cmd.value);
});
</script>
  
  
  
<style scoped>
</style>
  