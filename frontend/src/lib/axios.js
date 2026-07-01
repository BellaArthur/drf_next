import axios from 'axios'
import Cookies from 'js-cookie'

export const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000";


const api = axios.create({
    baseURL: process.env.NEXT_PUBLIC_API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
})

let isRefreshing  = false
let failedQueue   = []

const processQueue = (error, token = null) => {
    failedQueue.forEach(promise => {
        if (error) {
            promise.reject(error)
        } else {
            promise.resolve(token)
        }
    })
    failedQueue = []
}

// ─── Request interceptor ─────────────────────────────────────────────────────
api.interceptors.request.use(
    config => {
        const access = Cookies.get('access')
        if (access) {
            config.headers.Authorization = `Bearer ${access}`
        }
        return config
    },
    error => Promise.reject(error)
)

// ─── Response interceptor ────────────────────────────────────────────────────
api.interceptors.response.use(
    response => response,
    async error => {
        const originalRequest = error.config

        if (error.response?.status === 401 && !originalRequest._retry) {

            if (isRefreshing) {
                return new Promise((resolve, reject) => {
                    failedQueue.push({ resolve, reject })
                })
                .then(token => {
                    originalRequest.headers.Authorization = `Bearer ${token}`
                    return api(originalRequest)
                })
                .catch(err => Promise.reject(err))
            }

            originalRequest._retry = true
            isRefreshing = true

            try {
                const refresh = Cookies.get('refresh')

                if (!refresh) {
                    throw new Error('No refresh token')
                }

                const { data } = await axios.post(
                    `${process.env.NEXT_PUBLIC_API_URL}/auth/token/refresh/`,
                    { refresh }
                )

                Cookies.set('access',  data.access,  { secure: true, sameSite: 'strict' })
                Cookies.set('refresh', data.refresh, { secure: true, sameSite: 'strict' })

                processQueue(null, data.access)

                originalRequest.headers.Authorization = `Bearer ${data.access}`
                return api(originalRequest)

            } catch (refreshError) {
                processQueue(refreshError, null)
                Cookies.remove('access')
                Cookies.remove('refresh')
                window.location.href = '/login'
                return Promise.reject(refreshError)

            } finally {
                isRefreshing = false
            }
        }

        return Promise.reject(error)
    }
)

export default api