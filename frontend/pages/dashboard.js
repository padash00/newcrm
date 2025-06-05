import { useEffect, useState } from 'react'
import axios from 'axios'
import { useRouter } from 'next/router'

export default function Dashboard() {
  const [data, setData] = useState(null)
  const router = useRouter()

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
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  )
}
