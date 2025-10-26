'use client'

import React, { createContext, useContext, useState, useEffect } from 'react'
import { SimpleLogin, AuthResponse, User } from '@/types/api'
import { authAPI } from '@/lib/api'

interface AuthContextType {
  user: User | null
  isAuthenticated: boolean
  login: (credentials: SimpleLogin) => Promise<void>
  logout: () => void
  loading: boolean
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Check if user is already authenticated (for simple auth, we don't persist)
    setLoading(false)
  }, [])

  const login = async (credentials: SimpleLogin) => {
    try {
      setLoading(true)
      const response: AuthResponse = await authAPI.login(credentials)

      if (response.authenticated) {
        // For simple auth, create a basic user object
        const userData: User = {
          id: 1,
          username: "admin",
          email: credentials.email,
          role: "admin",
          is_active: true,
          created_at: new Date().toISOString()
        }

        setUser(userData)
        setIsAuthenticated(true)
      } else {
        throw new Error('Authentication failed')
      }
    } catch (error) {
      setIsAuthenticated(false)
      setUser(null)
      throw new Error('Invalid credentials')
    } finally {
      setLoading(false)
    }
  }

  const logout = () => {
    setIsAuthenticated(false)
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{ user, isAuthenticated, login, logout, loading }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}
