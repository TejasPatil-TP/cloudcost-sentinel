"use client"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1"

export default function IngestionPage() {
  const [file, setFile] = useState<File | null>(null)
  const [provider, setProvider] = useState("aws")
  const [status, setStatus] = useState("")

  const handleUpload = async () => {
    if (!file) return

    const formData = new FormData()
    formData.append("file", file)

    setStatus("Uploading...")
    try {
      const res = await fetch(`${API_URL}/upload/${provider}`, {
        method: "POST",
        body: formData,
      })
      
      if (res.ok) {
        setStatus("Upload successful! Processing started in background.")
      } else {
        setStatus("Upload failed.")
      }
    } catch (e) {
      setStatus("Error uploading file.")
    }
  }

  return (
    <div className="p-8">
      <h2 className="text-3xl font-bold tracking-tight mb-6">Data Ingestion</h2>
      <Card className="max-w-md">
        <CardHeader>
          <CardTitle>Upload Billing Export</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-1">Provider</label>
            <select 
              className="w-full border p-2 rounded" 
              value={provider} 
              onChange={e => setProvider(e.target.value)}
            >
              <option value="aws">AWS (Cost and Usage Report CSV)</option>
              <option value="azure">Azure (Cost Export CSV)</option>
              <option value="gcp">GCP (BigQuery Export CSV)</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">File</label>
            <input 
              type="file" 
              accept=".csv"
              className="w-full border p-2 rounded" 
              onChange={e => setFile(e.target.files?.[0] || null)} 
            />
          </div>
          <button 
            className="bg-blue-600 text-white px-4 py-2 rounded font-medium hover:bg-blue-700 disabled:opacity-50"
            onClick={handleUpload}
            disabled={!file}
          >
            Upload
          </button>
          {status && <p className="text-sm mt-2">{status}</p>}
        </CardContent>
      </Card>
      
      <Card className="max-w-md mt-8">
        <CardHeader>
          <CardTitle>Run Anomaly Detection</CardTitle>
        </CardHeader>
        <CardContent>
          <button 
            className="bg-red-600 text-white px-4 py-2 rounded font-medium hover:bg-red-700"
            onClick={async () => {
              await fetch(`${API_URL}/anomalies/detect`, { method: "POST" })
              alert("Anomaly detection job triggered.")
            }}
          >
            Trigger Job
          </button>
        </CardContent>
      </Card>
    </div>
  )
}
