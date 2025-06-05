bh21zy-codex/разработка-crm-системы-для-компьютерного-клуба

codex/разработка-crm-системы-для-компьютерного-клуба
main
import { useEffect, useState, useContext } from 'react'
import axios from 'axios'
import { useRouter } from 'next/router'
import { AuthContext } from '../context/AuthContext'

bh21zy-codex/разработка-crm-системы-для-компьютерного-клуба
export default function Dashboard() {
  const [data, setData] = useState(null)
  const router = useRouter()
  const { role } = useContext(AuthContext)

import { useEffect, useState } from 'react'
import axios from 'axios'
import { useRouter } from 'next/router'
main

export default function Dashboard() {
  const [data, setData] = useState(null)
  const router = useRouter()
codex/разработка-crm-системы-для-компьютерного-клуба
  const { role } = useContext(AuthContext)
main
main

  useEffect(() => {
    const token = localStorage.getItem('token')
    if (!token) { router.replace('/login'); return }
    axios.get('/api/protected', { headers: { Authorization: `Bearer ${token}` } })
      .then(res => setData(res.data))
      .catch(() => router.replace('/login'))
  }, [router])

  if (!data) return <div>Loading...</div>

  return (
    <div className="p-4">
      <h1 className="text-xl font-bold">Dashboard</h1>
bh21zy-codex/разработка-crm-системы-для-компьютерного-клуба

codex/разработка-crm-системы-для-компьютерного-клуба
main
      <p>Ваша роль: {role}</p>
      {role === 'tech' ? (
        <p>Технический режим: только статус ПК</p>
      ) : (
        <pre>{JSON.stringify(data, null, 2)}</pre>
      )}
bh21zy-codex/разработка-crm-системы-для-компьютерного-клуба


      <pre>{JSON.stringify(data, null, 2)}</pre>
main
main
    </div>
  )
}
