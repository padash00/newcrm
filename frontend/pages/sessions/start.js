import { useEffect, useState } from 'react'
import axios from 'axios'
import { useRouter } from 'next/router'
import { Button } from '../../components/ui/button'

export default function StartSession() {
  const [computers, setComputers] = useState([])
  const [tariffs, setTariffs] = useState([])
  const [clients, setClients] = useState([])
  const [computer, setComputer] = useState('')
  const [tariff, setTariff] = useState('')
  const [client, setClient] = useState('')
  const router = useRouter()

  useEffect(() => {
    const token = localStorage.getItem('token')
    if (!token) { router.replace('/login'); return }
    const headers = { Authorization: `Bearer ${token}` }
    axios.get('/api/computers', { headers }).then(res => setComputers(res.data))
    axios.get('/api/tariffs', { headers }).then(res => setTariffs(res.data))
    axios.get('/api/clients', { headers }).then(res => setClients(res.data))
  }, [router])

  const handleStart = async (e) => {
    e.preventDefault()
    const token = localStorage.getItem('token')
    try {
      await axios.post('/api/sessions/start', {
        computer_id: parseInt(computer),
        tariff_id: parseInt(tariff),
        client_id: parseInt(client)
      }, { headers: { Authorization: `Bearer ${token}` } })
      alert('Сессия запущена')
    } catch {
      alert('Ошибка запуска')
    }
  }

  return (
    <div className="p-4">
      <h1 className="text-xl font-bold mb-4">Запуск сессии</h1>
      <form onSubmit={handleStart} className="space-y-2">
        <select className="border p-2 w-full" value={computer} onChange={e => setComputer(e.target.value)}>
          <option value="">ПК</option>
          {computers.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}
        </select>
        <select className="border p-2 w-full" value={tariff} onChange={e => setTariff(e.target.value)}>
          <option value="">Тариф</option>
          {tariffs.map(t => <option key={t.id} value={t.id}>{t.name}</option>)}
        </select>
        <select className="border p-2 w-full" value={client} onChange={e => setClient(e.target.value)}>
          <option value="">Клиент</option>
          {clients.map(c => <option key={c.id} value={c.id}>{c.full_name}</option>)}
        </select>
        <Button type="submit">Старт</Button>
      </form>
    </div>
  )
}
