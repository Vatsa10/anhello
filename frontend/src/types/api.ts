// API Types
export interface User {
  id: number
  username: string
  email: string
  role: string
  is_active: boolean
  created_at: string
}

export interface Client {
  id: number
  name: string
  domain: string
  created_at: string
}

export interface BlogPost {
  id: number
  client_id: number
  author_id: number
  title: string
  content: string
  tags?: string
  category?: string
  featured_image?: string
  meta_description?: string
  slug: string
  status: string
  created_at: string
  updated_at?: string
  client?: Client
  author?: User
}

export interface BlogPostCreate {
  title: string
  content: string
  tags?: string
  category?: string
  featured_image?: string
  meta_description?: string
  slug: string
  status?: string
  client_id: number
}

export interface BlogPostUpdate {
  title?: string
  content?: string
  tags?: string
  category?: string
  featured_image?: string
  meta_description?: string
  slug?: string
  status?: string
}

export interface UserLogin {
  username: string
  password: string
}

export interface AuthResponse {
  access_token: string
  token_type: string
}

export interface ApiResponse<T> {
  data?: T
  message?: string
  error?: string
}
