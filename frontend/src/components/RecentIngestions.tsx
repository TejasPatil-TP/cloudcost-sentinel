"use client"
import { useEffect, useState } from "react"

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1"

type IngestionJob = { id: string, provider: string, file_name: string, status: string, records_processed: number }

export function RecentIngestions() {
  const [ingestions, setIngestions] = useState<IngestionJob[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch(`${API_URL}/ingestions`)
      .then(res => res.json())
      .then(d => {
        if (Array.isArray(d)) setIngestions(d)
        setLoading(false)
      })
      .catch(() => setLoading(false))
  }, [])

  if (loading) return <div>Loading recent ingestions...</div>
  if (ingestions.length === 0) return <div className="text-sm text-muted-foreground">No recent ingestions found.</div>

  return (
    <div className="space-y-8">
      {ingestions.map((job: {id: string, provider: string, file_name: string, status: string, records_processed: number}) => (
        <div key={job.id} className="flex items-center">
          <div className="ml-4 space-y-1">
            <p className="text-sm font-medium leading-none">{job.provider.toUpperCase()} Cost Export - {job.file_name}</p>
            <p className="text-sm text-muted-foreground">
              {job.status === "completed" ? `Processed ${job.records_processed} records` : job.status}
            </p>
          </div>
          <div className={`ml-auto font-medium ${job.status === 'completed' ? 'text-green-500' : 'text-red-500'}`}>
            {job.status.charAt(0).toUpperCase() + job.status.slice(1)}
          </div>
        </div>
      ))}
    </div>
  )
}


