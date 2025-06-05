import { useEffect, useState, useContext } from 'react'
import axios from 'axios'
import { useRouter } from 'next/router'
import { LineChart, Line, XAxis, YAxis, Tooltip, BarChart, Bar, PieChart, Pie, Cell } from 'recharts'
import { AuthContext } from '../context/AuthContext'

const COLORS = ['#8884d8', '#82ca9d', '#ff7300']

export default function Analytics() {
  const [income, setIncome] = useState([])
  const [clients, setClients] = useState([])
  const [paymentPie, setPaymentPie] = useState([])
  const [range, setRange] = useState(7)
  const router = useRouter()
  const { role } = useContext(AuthContext)

  useEffect(() => {
    const token = localStorage.getItem('token')
    if (!token) { router.replace('/login'); return }
    if (!['operator','admin'].includes(role)) return
    axios.get(`/api/reports/income-by-day?range=${range}`, { headers:{Authorization:`Bearer ${token}`}})
      .then(res => setIncome(res.data))
    axios.get(`/api/reports/clients-active?range=${range}`, { headers:{Authorization:`Bearer ${token}`}})
      .then(res => setClients(res.data))
    axios.get('/api/reports/daily', { headers:{Authorization:`Bearer ${token}`}})
      .then(res => {
        setPaymentPie([
          {name:'cash', value:res.total_cash},
          {name:'kaspi', value:res.total_kaspi},
          {name:'debt', value:res.total_debt}
        ])
      })
  }, [range, router, role])

  if (!['operator','admin'].includes(role)) return <div className="p-4">Нет доступа</div>

  return (
    <div className="p-4 space-y-4">
      <h1 className="text-xl font-bold">Аналитика</h1>
      <select className="border p-2" value={range} onChange={e=>setRange(e.target.value)}>
        <option value={7}>Неделя</option>
        <option value={30}>Месяц</option>
        <option value={90}>Квартал</option>
      </select>
      <LineChart width={600} height={300} data={income}>
        <XAxis dataKey="date" />
        <YAxis />
        <Tooltip />
        <Line dataKey="income" stroke="#8884d8" />
      </LineChart>
      <BarChart width={600} height={300} data={clients}>
        <XAxis dataKey="date" />
        <YAxis />
        <Tooltip />
        <Bar dataKey="clients" fill="#82ca9d" />
      </BarChart>
      <PieChart width={300} height={300}>
        <Pie data={paymentPie} dataKey="value" nameKey="name" label>
          {paymentPie.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
          ))}
        </Pie>
        <Tooltip />
      </PieChart>
    </div>
  )
}
