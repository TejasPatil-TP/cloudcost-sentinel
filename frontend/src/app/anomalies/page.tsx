"use client"

import { useEffect, useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1"

type AnomalyView = {
  id: string;
  provider: string;
  service: string;
  date: string;
  expected_cost: number;
  actual_cost: number;
  deviation_percentage: number;
  status: string;
}

export default function AnomaliesPage() {
  const [anomalies, setAnomalies] = useState<AnomalyView[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch(`${API_URL}/anomalies`)
      .then(res => res.json())
      .then(d => {
        if (Array.isArray(d)) setAnomalies(d)
        setLoading(false)
      })
      .catch(() => setLoading(false))
  }, [])

  return (
    <div className="p-8">
      <h2 className="text-3xl font-bold tracking-tight mb-6">Anomalies Detected</h2>
      
      {loading ? (
        <div>Loading anomalies...</div>
      ) : anomalies.length === 0 ? (
        <div className="text-muted-foreground">No anomalies detected.</div>
      ) : (
        <div className="space-y-4">
          {anomalies.map((a, i) => (
            <Card key={i} className="border-red-200 bg-red-50">
              <CardHeader>
                <CardTitle className="text-red-700">Spike in {a.provider.toUpperCase()} - {a.service}</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-3 gap-4">
                  <div>
                    <p className="text-sm text-red-600 font-medium">Actual Cost</p>
                    <p className="text-xl font-bold">${a.actual_cost.toFixed(2)}</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600 font-medium">Expected (7-day Avg)</p>
                    <p className="text-xl font-bold">${a.expected_cost.toFixed(2)}</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600 font-medium">Deviation</p>
                    <p className="text-xl font-bold">+{a.deviation_percentage.toFixed(1)}%</p>
                  </div>
                </div>
                <p className="text-sm text-gray-500 mt-4">Detected on: {a.date.split(' ')[0]}</p>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  )
}

