import { useParams, Link } from "react-router-dom"
import { useQuery } from "@tanstack/react-query"
import { getJob, getJobThumbnails } from "../api/jobs"
import ThumbnailCard from "../components/ThumbnailCard"

export default function JobDetail() {
  const { id } = useParams<{ id: string }>()

  const {
    data: job,
    isLoading,
    error,
  } = useQuery({
    queryKey: ["job", id],
    queryFn: () => getJob(id!),
    enabled: !!id,
    refetchInterval: ({ state }) =>
      state.data?.status === "pending" || state.data?.status === "processing" ? 3000 : false,
  })

  const { data: thumbnails } = useQuery({
    queryKey: ["job", id, "thumbnails"],
    queryFn: () => getJobThumbnails(id!),
    enabled: !!id,
    refetchInterval: ({ state }) =>
      state.data?.some((t) => t.status === "pending" || t.status === "processing")
        ? 3000
        : false,
  })

  if (isLoading) return <p className="loading">Loading job...</p>
  if (error || !job) return <p className="error">Job not found</p>

  return (
    <section className="page detail-page">
      <Link to="/" className="back-link">&larr; Back to jobs</Link>

      <div className="detail-header">
        <h1>Job Detail</h1>
        <span className={`status-badge ${job.status}`}>{job.status}</span>
      </div>

      <div className="detail-info">
        <p><strong>Prompt:</strong> {job.prompt}</p>
        <p><strong>Headshot:</strong> {job.headshot_url}</p>
        <p><strong>Thumbnails requested:</strong> {job.num_thumbnail}</p>
        <p><strong>Created:</strong> {new Date(job.created_at).toLocaleString()}</p>
      </div>

      <h2>Thumbnails</h2>
      {thumbnails && thumbnails.length > 0 ? (
        <div className="thumbnail-grid">
          {thumbnails.map((t) => (
            <ThumbnailCard key={t.id} thumbnail={t} />
          ))}
        </div>
      ) : (
        <p className="empty-state">No thumbnails generated yet.</p>
      )}
    </section>
  )
}
