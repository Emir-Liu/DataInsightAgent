
import axios from "axios"

// 后端地址

// const ip = process.env.VUE_APP_BACKEND_IP
const ip = import.meta.env.VITE_BACKEND_IP
// const port = process.env.VUE_APP_BACKEND_PORT
const port = import.meta.env.VITE_BACKEND_PORT
// export const DOMAIN = '172.22.0.90:9000'
export const DOMAIN = ip + ':' + port
export const baseUrl = 'http://' + DOMAIN
console.log('env:', import.meta.env)
console.log('backend ip:', ip)
console.log('backend port:', port)

axios.defaults.baseURL = baseUrl

// 对axio进行配置和封装
// GET请求
export function get(url: string, params: object) {
    // console.log('param:',params)
    return axios.get(url, { params })
        .then(function (res: any) {
            return res
        })
        .catch(function () {
            // 异常处理
        })
}

// POST请求
// 需要注意的是，POST请求发送的使用DataFrame，因为支持文件发送
export function post(url: string, params: object) {
    return axios.post(url, params)
        .then(function (res: any) { return res })
        .catch(function () {
            // 异常处理
        })
}
