export function Card({children, className=""}) {
  return (
    <div className={`bg-white shadow rounded-md border p-4 ${className}`}>{children}</div>
  )
}
