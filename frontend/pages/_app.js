import '../styles/globals.css'
codex/разработка-crm-системы-для-компьютерного-клуба
import { AuthProvider } from '../context/AuthContext'

export default function App({ Component, pageProps }) {
  return (
    <AuthProvider>
      <Component {...pageProps} />
    </AuthProvider>
  )


export default function App({ Component, pageProps }) {
  return <Component {...pageProps} />
main
}
