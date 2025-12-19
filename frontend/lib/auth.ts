import api from './api'

export interface LoginData {
  email: string
  password: string
  two_factor_code?: string
}

export interface User {
  id: number
  email: string
  name: string
  role: string
  user_type: 'legia_user' | 'tenant_user'
  tenant_id?: number
  tenant_name?: string
}

export interface AuthResponse {
  access_token: string
  refresh_token: string
  token_type: string
  user: User
}

export const authService = {
  async login(data: LoginData, tenantId?: number): Promise<AuthResponse> {
    const headers: any = {}
    if (tenantId) {
      headers['X-Tenant-ID'] = tenantId
    }

    const response = await api.post<AuthResponse>('/auth/login', data, { headers })
    return response.data
  },

  async logout() {
    try {
      await api.post('/auth/logout')
    } catch (error) {
      // Ignorar erros de logout
    } finally {
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      localStorage.removeItem('user')
    }
  },

  getCurrentUser(): User | null {
    if (typeof window === 'undefined') return null

    const userStr = localStorage.getItem('user')
    if (!userStr) return null

    try {
      return JSON.parse(userStr)
    } catch {
      return null
    }
  },

  isAuthenticated(): boolean {
    return !!localStorage.getItem('access_token')
  },

  isSuperAdmin(): boolean {
    const user = this.getCurrentUser()
    return user?.user_type === 'legia_user' && user?.role === 'superadmin'
  },

  isTenantUser(): boolean {
    const user = this.getCurrentUser()
    return user?.user_type === 'tenant_user'
  },
}
