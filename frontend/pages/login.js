bh21zy-codex/разработка-crm-системы-для-компьютерного-клуба

codex/разработка-crm-системы-для-компьютерного-клуба
main
import { useState, useContext } from 'react'
import axios from 'axios'
import { useRouter } from 'next/router'
import { AuthContext } from '../context/AuthContext'

bh21zy-codex/разработка-crm-системы-для-компьютерного-клуба

import { useState } from 'react'
import axios from 'axios'
import { useRouter } from 'next/router'
main

main
export default function Login() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const router = useRouter()
bh21zy-codex/разработка-crm-системы-для-компьютерного-клуба
  const { login } = useContext(AuthContext)

codex/разработка-crm-системы-для-компьютерного-клуба
  const { login } = useContext(AuthContext)
main
main

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      const res = await axios.post('/api/auth/login', { username, password })
bh21zy-codex/разработка-crm-системы-для-компьютерного-клуба
      login(res.data.access_token, res.data.role)

codex/разработка-crm-системы-для-компьютерного-клуба
      login(res.data.access_token, res.data.role)

      localStorage.setItem('token', res.data.access_token)
 main
main
      router.push('/dashboard')
    } catch (err) {
      alert('Login failed')
    }
  }

  return (
    <div className="flex h-screen items-center justify-center">
      <form onSubmit={handleSubmit} className="space-y-4">
        <input className="border p-2" placeholder="Username" value={username} onChange={e => setUsername(e.target.value)} />
        <input className="border p-2" type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} />
        <button className="bg-blue-500 text-white px-4 py-2" type="submit">Login</button>
      </form>
    </div>
  )
}
