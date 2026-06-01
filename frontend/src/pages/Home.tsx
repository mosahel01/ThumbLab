import { useQuery } from "@tanstack/react-query"
import { Link } from "react-router-dom"
import { listJobs } from "../api/jobs"
import JobCard from "../components/JobCard"

export default function Home() {
  const { data: jobs, isLoading, error } = useQuery({
    queryKey: ["jobs"],
    queryFn: listJobs,
  })

  return (
    <section className="page home-page">
      <div className="page-header">
        <h1>Thumbnail Jobs</h1>
        <Link to="/create" className="btn btn-primary">
          + New Job
        </Link>
      </div>

      {isLoading && <p className="loading">Loading jobs...</p>}

      {error && <p className="error">Failed to load jobs</p>}

      {jobs && jobs.length === 0 && (
        <div className="empty-state">
          <p>No jobs yet.</p>
          <Link to="/create" className="btn btn-primary">
            Create your first job
          </Link>
        </div>
      )}

      {jobs && jobs.length > 0 && (
        <div className="job-list">
          {jobs.map((job) => (
            <JobCard key={job.id} job={job} />
          ))}
        </div>
      )}
    </section>
  )
}
