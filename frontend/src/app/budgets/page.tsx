"use client"

import { useEffect, useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1"

type BudgetView = {
  name: string;
  amount: number;
  period: string;
  provider_filter?: string;
}

export default function BudgetsPage() {
  const [budgets, setBudgets] = useState<BudgetView[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch(`${API_URL}/budgets`)
      .then(res => res.json())
      .then(d => {
        if (Array.isArray(d)) setBudgets(d)
        setLoading(false)
      })
      .catch(() => setLoading(false))
  }, [])

  return (
    <div className="p-8">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-3xl font-bold tracking-tight">Budgets</h2>
        <button 
          className="bg-green-600 text-white px-4 py-2 rounded font-medium hover:bg-green-700"
          onClick={async () => {
            await fetch(`${API_URL}/budgets/seed`, { method: "POST" })
            window.location.reload()
          }}
        >
          Seed Sample Budgets
        </button>
      </div>
      
      {loading ? (
        <div>Loading budgets...</div>
      ) : budgets.length === 0 ? (
        <div className="text-muted-foreground">No budgets configured. Click &apos;Seed Sample Budgets&apos; to populate.</div>
      ) : (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {budgets.map((b, i) => (
            <Card key={i}>
              <CardHeader>
                <CardTitle>{b.name}</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">${b.amount.toLocaleString()}</div>
                <p className="text-sm text-muted-foreground">Period: {b.period}</p>
                {b.provider_filter && <p className="text-sm mt-2 font-medium">Provider: {b.provider_filter}</p>}
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  )
}


