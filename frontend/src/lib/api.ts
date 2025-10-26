import axios from 'axios'
import { User, Client, BlogPost, BlogPostCreate, BlogPostUpdate, SimpleLogin } from '@/types/api'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Simple authentication - no JWT tokens needed
export const authAPI = {
  login: async (credentials: SimpleLogin): Promise<{ message: string; email: string; authenticated: boolean }> => {
    const formData = new FormData()
    formData.append('email', credentials.email)
    formData.append('password', credentials.password)

    const response = await api.post('/login', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  },
  getCurrentUser: async (): Promise<User> => {
    // For simple auth, we'll use a different approach
    // Send credentials with each request as form data
    const formData = new FormData()
    formData.append('email', 'admin@example.com')
    formData.append('password', 'admin123')

    const response = await api.get('/users/me', { data: formData })
    return response.data
  },
}

// Clients API
export const clientsAPI = {
  getAll: async (): Promise<Client[]> => {
    const formData = new FormData()
    formData.append('email', 'admin@example.com')
    formData.append('password', 'admin123')

    const response = await api.get('/clients/', { data: formData })
    return response.data
  },
  getById: async (id: number): Promise<Client> => {
    const formData = new FormData()
    formData.append('email', 'admin@example.com')
    formData.append('password', 'admin123')

    const response = await api.get(`/clients/${id}`, { data: formData })
    return response.data
  },
  create: async (client: Omit<Client, 'id' | 'created_at'>): Promise<Client> => {
    const formData = new FormData()
    formData.append('email', 'admin@example.com')
    formData.append('password', 'admin123')
    formData.append('name', client.name)
    formData.append('domain', client.domain)

    const response = await api.post('/clients/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
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
    const formData = new FormData()
    formData.append('email', 'admin@example.com')
    formData.append('password', 'admin123')

    const response = await api.get('/blogs/', {
      data: formData,
      params
    })
    return response.data
  },
  getById: async (id: number): Promise<BlogPost> => {
    const formData = new FormData()
    formData.append('email', 'admin@example.com')
    formData.append('password', 'admin123')

    const response = await api.get(`/blogs/${id}`, { data: formData })
    return response.data
  },
  create: async (blogPost: BlogPostCreate): Promise<BlogPost> => {
    const formData = new FormData()
    formData.append('email', 'admin@example.com')
    formData.append('password', 'admin123')

    Object.keys(blogPost).forEach(key => {
      const value = blogPost[key as keyof BlogPostCreate]
      if (value !== undefined) {
        formData.append(key, String(value))
      }
    })

    const response = await api.post('/blogs/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  },
  update: async (id: number, blogPost: BlogPostUpdate): Promise<BlogPost> => {
    const formData = new FormData()
    formData.append('email', 'admin@example.com')
    formData.append('password', 'admin123')

    Object.keys(blogPost).forEach(key => {
      const value = blogPost[key as keyof BlogPostUpdate]
      if (value !== undefined) {
        formData.append(key, String(value))
      }
    })

    const response = await api.put(`/blogs/${id}`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  },
  delete: async (id: number): Promise<{ message: string }> => {
    const formData = new FormData()
    formData.append('email', 'admin@example.com')
    formData.append('password', 'admin123')

    const response = await api.delete(`/blogs/${id}`, { data: formData })
    return response.data
  },
}

// File upload API
export const uploadAPI = {
  uploadImage: async (file: File): Promise<{ filename: string; url: string; message: string }> => {
    const formData = new FormData()
    formData.append('email', 'admin@example.com')
    formData.append('password', 'admin123')
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
