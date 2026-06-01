import { Link } from "react-router-dom"
import type { Job } from "../types"

const statusColors: Record<string, string> = {
  pending: "var(--text)",
  processing: "#eab308",
  completed: "#22c55e",
  failed: "#ef4444",
}

export default function JobCard({ job }: { job: Job }) {
  return (
    <Link to={`/jobs/${job.id}`} className="job-card">
      <p className="job-prompt">{job.prompt}</p>
      <div className="job-meta">
        <span
          className="job-status"
          style={{ color: statusColors[job.status] }}
        >
          {job.status}
        </span>
        <span>{job.num_thumbnail} thumbnail{job.num_thumbnail > 1 ? "s" : ""}</span>
        <span>{new Date(job.created_at).toLocaleDateString()}</span>
      </div>
    </Link>
  )
}
