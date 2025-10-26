'use client'

import React, { createContext, useContext, useState, useEffect } from 'react'
import { User, UserLogin, AuthResponse } from '@/types/api'
import { authAPI } from '@/lib/api'

interface AuthContextType {
  user: User | null
  token: string | null
  login: (credentials: UserLogin) => Promise<void>
  logout: () => void
  loading: boolean
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [token, setToken] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Check if user is logged in on mount
    const storedToken = localStorage.getItem('token')
    if (storedToken) {
      setToken(storedToken)
      // Fetch current user
      authAPI.getCurrentUser()
        .then(setUser)
        .catch(() => {
          // Token is invalid, remove it
          localStorage.removeItem('token')
          setToken(null)
        })
        .finally(() => setLoading(false))
    } else {
      setLoading(false)
    }
  }, [])

  const login = async (credentials: UserLogin) => {
    try {
      const response: AuthResponse = await authAPI.login(credentials)
      localStorage.setItem('token', response.access_token)
      setToken(response.access_token)

      // Fetch user data
      const userData = await authAPI.getCurrentUser()
      setUser(userData)
    } catch (error) {
      throw new Error('Invalid credentials')
    }
  }

  const logout = () => {
    localStorage.removeItem('token')
    setToken(null)
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{ user, token, login, logout, loading }}>
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
