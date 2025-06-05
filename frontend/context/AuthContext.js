import { createContext, useState, useEffect } from 'react'

export const AuthContext = createContext({ role: null })

export function AuthProvider({ children }) {
  const [role, setRole] = useState(null)

  useEffect(() => {
    const stored = localStorage.getItem('role')
    if (stored) setRole(stored)
  }, [])

  const login = (token, userRole) => {
    localStorage.setItem('token', token)
    localStorage.setItem('role', userRole)
    setRole(userRole)
  }

  const logout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('role')
    setRole(null)
  }

  return (
    <AuthContext.Provider value={{ role, login, logout }}>
      {children}
    </AuthContext.Provider>
  )
}
