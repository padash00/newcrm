import '../styles/globals.css'
bh21zy-codex/разработка-crm-системы-для-компьютерного-клуба

codex/разработка-crm-системы-для-компьютерного-клуба
 main
import { AuthProvider } from '../context/AuthContext'

export default function App({ Component, pageProps }) {
  return (
    <AuthProvider>
      <Component {...pageProps} />
    </AuthProvider>
  )
bh21zy-codex/разработка-crm-системы-для-компьютерного-клуба



export default function App({ Component, pageProps }) {
  return <Component {...pageProps} />
main
main
}
