export function Badge({children, className=""}) {
  return <span className={`px-2 py-1 text-xs rounded-full bg-gray-100 ${className}`}>{children}</span>
}
