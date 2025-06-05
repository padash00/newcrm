import { useEffect, useState, useRef } from 'react'
import axios from 'axios'
import { useRouter } from 'next/router'
import { Card } from '../components/ui/card'
import { Table, TableHeader, TableHead, TableBody, TableRow, TableCell } from '../components/ui/table'
import { Badge } from '../components/ui/badge'
import { Button } from '../components/ui/button'

export default function Clients() {
  const [clients, setClients] = useState([])
  const fileInput = useRef()
  const router = useRouter()

  useEffect(() => {
    const token = localStorage.getItem('token')
    if (!token) { router.replace('/login'); return }
    axios.get('/api/clients/', { headers: { Authorization: `Bearer ${token}` } })
      .then(res => setClients(res.data))
      .catch(() => router.replace('/login'))
  }, [router])

  const handleImport = async (e) => {
    const file = e.target.files[0]
    if (!file) return
    const token = localStorage.getItem('token')
    const form = new FormData()
    form.append('file', file)
    try {
      const res = await axios.post('/api/clients/import_excel', form, {
        headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'multipart/form-data' }
      })
      alert(`Добавлено: ${res.data.added}\nОшибки: ${res.data.errors.join('\n')}`)
      const list = await axios.get('/api/clients/', { headers: { Authorization: `Bearer ${token}` } })
      setClients(list.data)
    } catch {
      alert('Ошибка импорта')
    }
  }

  return (
    <div className="p-4 space-y-4">
      <h1 className="text-xl font-bold">Клиенты</h1>
      <div className="flex items-center space-x-2">
        <Button onClick={() => fileInput.current.click()}>Импорт из Excel</Button>
        <input type="file" accept=".xlsx" ref={fileInput} className="hidden" onChange={handleImport} />
      </div>
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
