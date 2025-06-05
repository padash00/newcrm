export function Table({children, className=""}) {
  return <table className={`min-w-full text-sm ${className}`}>{children}</table>
}
export const TableHeader = ({children}) => <thead className="bg-gray-50">{children}</thead>
export const TableBody = ({children}) => <tbody>{children}</tbody>
export const TableRow = ({children, className=""}) => <tr className={`border-b ${className}`}>{children}</tr>
export const TableHead = ({children, className=""}) => <th className={`px-2 py-1 text-left ${className}`}>{children}</th>
export const TableCell = ({children, className=""}) => <td className={`px-2 py-1 ${className}`}>{children}</td>
