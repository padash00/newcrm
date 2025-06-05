import { useEffect, useState, useContext } from 'react'
import axios from 'axios'
import { useRouter } from 'next/router'
import { LineChart, Line, XAxis, YAxis, Tooltip, BarChart, Bar } from 'recharts'
import { AuthContext } from '../context/AuthContext'

export default function Reports() {
  const [data, setData] = useState([])
  const [mode, setMode] = useState('weekly')
  const [from, setFrom] = useState('')
  const [to, setTo] = useState('')
  const router = useRouter()
  const { role } = useContext(AuthContext)

  useEffect(() => {
    const token = localStorage.getItem('token')
    if (!token) { router.replace('/login'); return }
    if (!['operator','admin'].includes(role)) return
    let url = '/api/reports/weekly'
    if (mode === 'custom' && from && to) {
      url = `/api/reports/custom?from=${from}&to=${to}`
    }
    axios.get(url, { headers: { Authorization: `Bearer ${token}` } })
      .then(res => setData(res.data))
      .catch(() => router.replace('/login'))
  }, [mode, from, to, router, role])

  if (!['operator','admin'].includes(role)) return <div className="p-4">Нет доступа</div>

  return (
    <div className="p-4 space-y-4">
      <h1 className="text-xl font-bold">Отчёты</h1>
      <div className="space-x-2">
        <select className="border p-2" value={mode} onChange={e=>setMode(e.target.value)}>
          <option value="weekly">Неделя</option>
          <option value="custom">Диапазон</option>
        </select>
        {mode==='custom' && (
          <>
            <input type="date" className="border p-2" value={from} onChange={e=>setFrom(e.target.value)} />
            <input type="date" className="border p-2" value={to} onChange={e=>setTo(e.target.value)} />
          </>
        )}
      </div>
      <LineChart width={600} height={300} data={data}>
        <XAxis dataKey="date" />
        <YAxis />
        <Tooltip />
        <Line dataKey="total_kaspi" stroke="#8884d8" name="Kaspi" />
        <Line dataKey="total_cash" stroke="#82ca9d" name="Нал" />
        <Line dataKey="total_debt" stroke="#ff7300" name="Долг" />
      </LineChart>
      <BarChart width={600} height={200} data={data}>
        <XAxis dataKey="date" />
        <YAxis />
        <Tooltip />
        <Bar dataKey="total_sessions" fill="#8884d8" name="Сессии" />
      </BarChart>
    </div>
  )
}
