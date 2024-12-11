// 后端的API接口
// import { post } from 'node_modules/axios/index.cjs'
import { get } from './http'
const api_request = {
    Test: {
        test() {
            return get('/', {})
        }
    }
}

export default api_request