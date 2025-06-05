import { useEffect, useState } from 'react'
import axios from 'axios'
import { useRouter } from 'next/router'
import { Card } from '../components/ui/card'
import { Table, TableHeader, TableHead, TableBody, TableRow, TableCell } from '../components/ui/table'
import { Badge } from '../components/ui/badge'

export default function Clients() {
  const [clients, setClients] = useState([])
  const router = useRouter()

  useEffect(() => {
    const token = localStorage.getItem('token')
    if (!token) { router.replace('/login'); return }
    axios.get('/api/clients/', { headers: { Authorization: `Bearer ${token}` } })
      .then(res => setClients(res.data))
      .catch(() => router.replace('/login'))
  }, [router])

  return (
    <div className="p-4 space-y-4">
      <h1 className="text-xl font-bold">Клиенты</h1>
      <Card>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>ID</TableHead>
              <TableHead>ФИО</TableHead>
              <TableHead>Телефон</TableHead>
              <TableHead>Баланс</TableHead>
              <TableHead>Долг</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {clients.map(c => (
              <TableRow key={c.id} className="text-center">
                <TableCell>{c.id}</TableCell>
                <TableCell>{c.full_name}</TableCell>
                <TableCell>{c.phone}</TableCell>
                <TableCell>{c.balance}</TableCell>
                <TableCell>
                  {c.debt > 0 ? <Badge className="bg-red-100 text-red-800">{c.debt}</Badge> : c.debt}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </Card>
    </div>
  )
}
