import axios from 'axios'

// Função que retorna URL do backend baseado no ambiente ATUAL
const getBaseURL = () => {
  // 1. Se tem variável de ambiente, usar ela
  if (process.env.NEXT_PUBLIC_API_URL) {
    return process.env.NEXT_PUBLIC_API_URL
  }

  // 2. Se está no servidor (SSR), usar produção
  if (typeof window === 'undefined') {
    return 'https://legia-backend.onrender.com'
  }

  // 3. Se está no browser em localhost, usar local
  if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    return 'http://localhost:8000'
  }

  // 4. Qualquer outro caso (produção no browser), usar Render
  return 'https://legia-backend.onrender.com'
}

export const api = axios.create({
  baseURL: `${getBaseURL()}/api/v1`,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true,
})

// Interceptor para adicionar token automaticamente
api.interceptors.request.use((config) => {
  if (typeof window !== 'undefined') {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
  }
  return config
})

// Interceptor para renovar token se expirado
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      try {
        const refreshToken = localStorage.getItem('refresh_token')
        if (!refreshToken) throw new Error('No refresh token')

        const response = await axios.post(`${API_URL}/api/v1/auth/refresh`, {
          refresh_token: refreshToken,
        })

        const { access_token, refresh_token: newRefreshToken } = response.data

        localStorage.setItem('access_token', access_token)
        localStorage.setItem('refresh_token', newRefreshToken)

        originalRequest.headers.Authorization = `Bearer ${access_token}`
        return api(originalRequest)
      } catch (refreshError) {
        // Se falhar ao renovar, fazer logout
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        localStorage.removeItem('user')
        window.location.href = '/login'
        return Promise.reject(refreshError)
      }
    }

    return Promise.reject(error)
  }
)

export default api
