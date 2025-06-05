import { useEffect, useState, useContext } from 'react'
import axios from 'axios'
import { useRouter } from 'next/router'
import { Card } from '../components/ui/card'
import { Table, TableHeader, TableHead, TableBody, TableRow, TableCell } from '../components/ui/table'
import { Badge } from '../components/ui/badge'
import { Button } from '../components/ui/button'

import { AuthContext } from '../context/AuthContext'
export default function Bookings() {
  const [bookings, setBookings] = useState([])
  const [date, setDate] = useState('')
  const router = useRouter()
  const { role } = useContext(AuthContext)

  useEffect(() => {
    const token = localStorage.getItem('token')
    if (!token) { router.replace('/login'); return }
    if (!['operator','admin'].includes(role)) { setBookings([]); return }
    const params = date ? { date } : {}
    axios.get('/api/bookings/', { params, headers: { Authorization: `Bearer ${token}` } })
      .then(res => setBookings(res.data))
      .catch(() => router.replace('/login'))
  }, [router, date, role])
  if (!["operator","admin"].includes(role)) return <div className="p-4">Нет доступа</div>

  return (
    <div className="p-4 space-y-4">
      <h1 className="text-xl font-bold">Бронирования</h1>
      <div className="flex items-center space-x-2">
        <input type="date" className="border p-2" value={date} onChange={e => setDate(e.target.value)} />
        <Button onClick={() => setDate('')}>Сброс</Button>
      </div>
      <Card>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Клиент</TableHead>
              <TableHead>Зона</TableHead>
              <TableHead>ПК</TableHead>
              <TableHead>Время</TableHead>
              <TableHead>Длительность</TableHead>
              <TableHead>Статус</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {bookings.map(b => (
              <TableRow key={b.id} className="text-center">
                <TableCell>{b.client_id}</TableCell>
                <TableCell>{b.zone_id}</TableCell>
                <TableCell>{b.num_pcs}</TableCell>
                <TableCell>{b.start_time}</TableCell>
                <TableCell>{b.duration}</TableCell>
                <TableCell><Badge>{b.status}</Badge></TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </Card>
    </div>
  )
}
