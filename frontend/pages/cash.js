import { useState } from 'react'
import axios from 'axios'
import { useRouter } from 'next/router'

export default function Cash() {
  const [kaspi, setKaspi] = useState(0)
  const [cash, setCash] = useState(0)
  const [coins, setCoins] = useState(0)
  const [debt, setDebt] = useState(0)
  const [comment, setComment] = useState('')
  const router = useRouter()

  const handleSubmit = async (e) => {
    e.preventDefault()
    const token = localStorage.getItem('token')
    if (!token) { router.replace('/login'); return }
    try {
      await axios.post('/api/shifts/close', {
        kaspi_amount: parseFloat(kaspi),
        cash_amount: parseFloat(cash),
        coins_amount: parseFloat(coins),
        debt_amount: parseFloat(debt),
        comment
      }, { headers: { Authorization: `Bearer ${token}` } })
      alert('Смена закрыта')
    } catch (err) {
      alert('Ошибка')
    }
  }

  return (
    <div className="p-4">
      <h1 className="text-xl font-bold mb-4">Закрытие смены</h1>
      <form onSubmit={handleSubmit} className="space-y-2">
        <input className="border p-2 w-full" placeholder="Kaspi" type="number" value={kaspi} onChange={e => setKaspi(e.target.value)} />
        <input className="border p-2 w-full" placeholder="Нал" type="number" value={cash} onChange={e => setCash(e.target.value)} />
        <input className="border p-2 w-full" placeholder="Мелочь" type="number" value={coins} onChange={e => setCoins(e.target.value)} />
        <input className="border p-2 w-full" placeholder="Долги" type="number" value={debt} onChange={e => setDebt(e.target.value)} />
        <textarea className="border p-2 w-full" placeholder="Комментарий" value={comment} onChange={e => setComment(e.target.value)} />
        <button className="bg-blue-500 text-white px-4 py-2" type="submit">Закрыть</button>
      </form>
    </div>
  )
}
