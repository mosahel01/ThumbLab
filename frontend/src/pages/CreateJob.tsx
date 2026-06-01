import { useState } from "react"
import { useNavigate } from "react-router-dom"
import { useMutation, useQueryClient } from "@tanstack/react-query"
import { createJob } from "../api/jobs"

export default function CreateJob() {
  const navigate = useNavigate()
  const queryClient = useQueryClient()
  const [prompt, setPrompt] = useState("")
  const [headshotUrl, setHeadshotUrl] = useState("")
  const [numThumbnail, setNumThumbnail] = useState(1)

  const mutation = useMutation({
    mutationFn: createJob,
    onSuccess: (job) => {
      queryClient.invalidateQueries({ queryKey: ["jobs"] })
      navigate(`/jobs/${job.id}`)
    },
  })

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    mutation.mutate({ prompt, headshot_url: headshotUrl, num_thumbnail: numThumbnail })
  }

  return (
    <section className="page create-page">
      <h1>New Thumbnail Job</h1>
      <form onSubmit={handleSubmit} className="create-form">
        <label>
          Prompt
          <textarea
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="Describe the thumbnail you want..."
            required
          />
        </label>

        <label>
          Headshot URL
          <input
            type="url"
            value={headshotUrl}
            onChange={(e) => setHeadshotUrl(e.target.value)}
            placeholder="https://example.com/headshot.jpg"
            required
          />
        </label>

        <label>
          Number of thumbnails (1-3)
          <input
            type="number"
            min={1}
            max={3}
            value={numThumbnail}
            onChange={(e) => setNumThumbnail(Number(e.target.value))}
          />
        </label>

        <button type="submit" className="btn btn-primary" disabled={mutation.isPending}>
          {mutation.isPending ? "Creating..." : "Create Job"}
        </button>

        {mutation.error && <p className="error">Failed to create job</p>}
      </form>
    </section>
  )
}
