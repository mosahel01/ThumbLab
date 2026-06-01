import type { CreateJobPayload, Job, Thumbnail } from "../types"
import { request } from "./client"

export function listJobs(): Promise<Job[]> {
  return request("/jobs")
}

export function getJob(id: string): Promise<Job> {
  return request(`/jobs/${id}`)
}

export function createJob(payload: CreateJobPayload): Promise<Job> {
  return request("/jobs", {
    method: "POST",
    body: JSON.stringify(payload),
  })
}

export function getJobThumbnails(jobId: string): Promise<Thumbnail[]> {
  return request(`/jobs/${jobId}/thumbnails`)
}
