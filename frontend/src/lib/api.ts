import axios from 'axios'
import { UserLogin, AuthResponse, User, Client, BlogPost, BlogPostCreate, BlogPostUpdate } from '@/types/api'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Auth API
export const authAPI = {
  login: async (credentials: UserLogin): Promise<AuthResponse> => {
    const response = await api.post('/token', credentials)
    return response.data
  },
  getCurrentUser: async (): Promise<User> => {
    const response = await api.get('/users/me')
    return response.data
  },
}

// Clients API
export const clientsAPI = {
  getAll: async (): Promise<Client[]> => {
    const response = await api.get('/clients/')
    return response.data
  },
  getById: async (id: number): Promise<Client> => {
    const response = await api.get(`/clients/${id}`)
    return response.data
  },
  create: async (client: Omit<Client, 'id' | 'created_at'>): Promise<Client> => {
    const response = await api.post('/clients/', client)
    return response.data
  },
}

// Blog Posts API
export const blogPostsAPI = {
  getAll: async (params?: {
    skip?: number
    limit?: number
    client_id?: number
    status?: string
    search?: string
  }): Promise<BlogPost[]> => {
    const response = await api.get('/blogs/', { params })
    return response.data
  },
  getById: async (id: number): Promise<BlogPost> => {
    const response = await api.get(`/blogs/${id}`)
    return response.data
  },
  create: async (blogPost: BlogPostCreate): Promise<BlogPost> => {
    const response = await api.post('/blogs/', blogPost)
    return response.data
  },
  update: async (id: number, blogPost: BlogPostUpdate): Promise<BlogPost> => {
    const response = await api.put(`/blogs/${id}`, blogPost)
    return response.data
  },
  delete: async (id: number): Promise<{ message: string }> => {
    const response = await api.delete(`/blogs/${id}`)
    return response.data
  },
}

// File upload API
export const uploadAPI = {
  uploadImage: async (file: File): Promise<{ filename: string; url: string; message: string }> => {
    const formData = new FormData()
    formData.append('file', file)

    const response = await api.post('/upload/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  },
}

export default api
