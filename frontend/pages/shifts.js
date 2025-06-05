import { useEffect, useState } from 'react'
import axios from 'axios'
import { useRouter } from 'next/router'
import { Card } from '../components/ui/card'
import { Table, TableHeader, TableHead, TableBody, TableRow, TableCell } from '../components/ui/table'
import { Button } from '../components/ui/button'

export default function Shifts() {
  const [shifts, setShifts] = useState([])
  const [date, setDate] = useState('')
  const router = useRouter()

  useEffect(() => {
    const token = localStorage.getItem('token')
    if (!token) { router.replace('/login'); return }
    const params = date ? { date } : {}
    axios.get('/api/shifts/', { params, headers: { Authorization: `Bearer ${token}` } })
      .then(res => setShifts(res.data))
      .catch(() => router.replace('/login'))
  }, [router, date])

  return (
    <div className="p-4 space-y-4">
      <h1 className="text-xl font-bold">История смен</h1>
      <div className="flex items-center space-x-2">
        <input type="date" className="border p-2" value={date} onChange={e => setDate(e.target.value)} />
        <Button onClick={() => setDate('')}>Сброс</Button>
      </div>
      <Card>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Оператор</TableHead>
              <TableHead>Начало</TableHead>
              <TableHead>Конец</TableHead>
              <TableHead>Kaspi</TableHead>
              <TableHead>Наличные</TableHead>
              <TableHead>Долг</TableHead>
              <TableHead>Мелочь</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {shifts.map(s => (
              <TableRow key={s.id} className="text-center">
                <TableCell>{s.operator_id}</TableCell>
                <TableCell>{s.start_time}</TableCell>
                <TableCell>{s.end_time || '-'}</TableCell>
                <TableCell>{s.kaspi_amount}</TableCell>
                <TableCell>{s.cash_amount}</TableCell>
                <TableCell>{s.debt_amount}</TableCell>
                <TableCell>{s.coins_amount}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </Card>
    </div>
  )
}
