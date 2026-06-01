export interface Thumbnail {
  id: string
  job_id: string
  style_name: string
  image_url: string
  status: "pending" | "processing" | "completed" | "failed"
  error_message: string | null
  created_at: string
}

export interface Job {
  id: string
  prompt: string
  num_thumbnail: number
  headshot_url: string
  status: "pending" | "processing" | "completed" | "failed"
  created_at: string
  thumbnails?: Thumbnail[]
}

export interface CreateJobPayload {
  prompt: string
  num_thumbnail: number
  headshot_url: string
}
