"use client"

import { useEffect, useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Overview } from "@/components/Overview"
import { RecentIngestions } from "@/components/RecentIngestions"

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1"

type CostSummary = { provider: string, total_cost: number }
type AnomalyView = { id: string }

export default function Dashboard() {
  const [costs, setCosts] = useState<CostSummary[]>([])
  const [anomalies, setAnomalies] = useState<AnomalyView[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    Promise.all([
      fetch(`${API_URL}/costs`).then(r => r.json()).catch(() => []),
      fetch(`${API_URL}/anomalies`).then(r => r.json()).catch(() => [])
    ]).then(([costsData, anomaliesData]) => {
      setCosts(costsData)
      setAnomalies(anomaliesData)
      setLoading(false)
    })
  }, [])

  const awsCost = costs.find(c => c.provider === "aws")?.total_cost || 0
  const azureCost = costs.find(c => c.provider === "azure")?.total_cost || 0
  const gcpCost = costs.find(c => c.provider === "gcp")?.total_cost || 0

  if (loading) return <div className="p-8">Loading dashboard data...</div>

  return (
    <div className="flex-col md:flex">
      <div className="flex-1 space-y-4 p-8 pt-6">
        <div className="flex items-center justify-between space-y-2">
          <h2 className="text-3xl font-bold tracking-tight">CloudCost Sentinel Dashboard</h2>
        </div>
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                Total AWS Spend
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">${awsCost.toFixed(2)}</div>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                Total Azure Spend
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">${azureCost.toFixed(2)}</div>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                Total GCP Spend
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">${gcpCost.toFixed(2)}</div>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                Anomalies Detected
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-red-500">{anomalies.length}</div>
            </CardContent>
          </Card>
        </div>
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-7">
          <Card className="col-span-4">
            <CardHeader>
              <CardTitle>Spending Overview</CardTitle>
            </CardHeader>
            <CardContent className="pl-2">
              <Overview />
            </CardContent>
          </Card>
          <Card className="col-span-3">
            <CardHeader>
              <CardTitle>Recent Ingestions</CardTitle>
            </CardHeader>
            <CardContent>
              <RecentIngestions />
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}

