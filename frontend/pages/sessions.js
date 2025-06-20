bh21zy-codex/разработка-crm-системы-для-компьютерного-клуба

codex/разработка-crm-системы-для-компьютерного-клуба
main
import { useEffect, useState, useContext } from 'react'
import axios from 'axios'
import { useRouter } from 'next/router'
import { AuthContext } from '../context/AuthContext'
 bh21zy-codex/разработка-crm-системы-для-компьютерного-клуба


import { useEffect, useState } from 'react'
import axios from 'axios'
import { useRouter } from 'next/router'
main
main
import { Card } from '../components/ui/card'
import { Table, TableHeader, TableHead, TableBody, TableRow, TableCell } from '../components/ui/table'
import { Badge } from '../components/ui/badge'

export default function Sessions() {
  const [sessions, setSessions] = useState([])
  const router = useRouter()
bh21zy-codex/разработка-crm-системы-для-компьютерного-клуба
  const { role } = useContext(AuthContext)

codex/разработка-crm-системы-для-компьютерного-клуба
  const { role } = useContext(AuthContext)
main
main

  useEffect(() => {
    const token = localStorage.getItem('token')
    if (!token) { router.replace('/login'); return }
bh21zy-codex/разработка-crm-системы-для-компьютерного-клуба

codex/разработка-crm-системы-для-компьютерного-клуба
 main
    if (!['operator','admin'].includes(role)) { setSessions([]); return }
    axios.get('/api/sessions', { headers: { Authorization: `Bearer ${token}` } })
      .then(res => setSessions(res.data))
      .catch(() => router.replace('/login'))
  }, [router, role])

  if (!['operator','admin'].includes(role)) return <div className="p-4">Нет доступа</div>

bh21zy-codex/разработка-crm-системы-для-компьютерного-клуба

    axios.get('/api/sessions', { headers: { Authorization: `Bearer ${token}` } })
      .then(res => setSessions(res.data))
      .catch(() => router.replace('/login'))
  }, [router])
main

main
  return (
    <div className="p-4 space-y-4">
      <h1 className="text-xl font-bold">Сессии</h1>
      <Card>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>ПК</TableHead>
              <TableHead>Клиент</TableHead>
              <TableHead>Тариф</TableHead>
              <TableHead>Начало</TableHead>
              <TableHead>Конец</TableHead>
              <TableHead>Стоимость</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {sessions.map(s => (
              <TableRow key={s.id} className="text-center">
                <TableCell>{s.computer_id}</TableCell>
                <TableCell>{s.client_id}</TableCell>
                <TableCell>{s.tariff_id}</TableCell>
                <TableCell>{s.start_time}</TableCell>
                <TableCell>{s.end_time || <Badge className="bg-green-100 text-green-800">активна</Badge>}</TableCell>
                <TableCell>{s.cost}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </Card>
    </div>
  )
}
