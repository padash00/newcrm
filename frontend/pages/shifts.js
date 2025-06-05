bh21zy-codex/разработка-crm-системы-для-компьютерного-клуба
import { useEffect, useState, useContext } from 'react'

codex/разработка-crm-системы-для-компьютерного-клуба
import { useEffect, useState, useContext } from 'react'

import { useEffect, useState } from 'react'
main
main
import axios from 'axios'
import { useRouter } from 'next/router'
import { Card } from '../components/ui/card'
import { Table, TableHeader, TableHead, TableBody, TableRow, TableCell } from '../components/ui/table'
import { Button } from '../components/ui/button'

bh21zy-codex/разработка-crm-системы-для-компьютерного-клуба
import { AuthContext } from '../context/AuthContext'

codex/разработка-crm-системы-для-компьютерного-клуба
import { AuthContext } from '../context/AuthContext'
main
main
export default function Shifts() {
  const [shifts, setShifts] = useState([])
  const [date, setDate] = useState('')
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
    if (!['operator','admin'].includes(role)) { setShifts([]); return }

codex/разработка-crm-системы-для-компьютерного-клуба
    if (!['operator','admin'].includes(role)) { setShifts([]); return }
 main
 main
    const params = date ? { date } : {}
    axios.get('/api/shifts/', { params, headers: { Authorization: `Bearer ${token}` } })
      .then(res => setShifts(res.data))
      .catch(() => router.replace('/login'))
bh21zy-codex/разработка-crm-системы-для-компьютерного-клуба

 codex/разработка-crm-системы-для-компьютерного-клуба
main
  }, [router, date, role])

  const downloadExcel = async () => {
    const token = localStorage.getItem('token')
    try {
      const res = await axios.get('/api/shifts/export_excel', {
        headers: { Authorization: `Bearer ${token}` },
        responseType: 'blob'
      })
      const url = window.URL.createObjectURL(new Blob([res.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', 'shifts.xlsx')
      document.body.appendChild(link)
      link.click()
      link.remove()
    } catch {
      alert('Не удалось скачать файл')
    }
  }
  if (!["operator","admin"].includes(role)) return <div className="p-4">Нет доступа</div>

bh21zy-codex/разработка-crm-системы-для-компьютерного-клуба

  }, [router, date])
 main

main
  return (
    <div className="p-4 space-y-4">
      <h1 className="text-xl font-bold">История смен</h1>
      <div className="flex items-center space-x-2">
        <input type="date" className="border p-2" value={date} onChange={e => setDate(e.target.value)} />
        <Button onClick={() => setDate('')}>Сброс</Button>
bh21zy-codex/разработка-crm-системы-для-компьютерного-клуба
        <Button onClick={downloadExcel}>📥 Скачать отчёт</Button>

codex/разработка-crm-системы-для-компьютерного-клуба
        <Button onClick={downloadExcel}>📥 Скачать отчёт</Button>
main
main
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
