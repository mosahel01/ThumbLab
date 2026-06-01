import type { Thumbnail } from "../types"

const statusColors: Record<string, string> = {
  pending: "var(--text)",
  processing: "#eab308",
  completed: "#22c55e",
  failed: "#ef4444",
}

export default function ThumbnailCard({ thumbnail }: { thumbnail: Thumbnail }) {
  return (
    <div className="thumbnail-card">
      <div className="thumbnail-placeholder">
        {thumbnail.status === "completed" && thumbnail.image_url ? (
          <img
            src={thumbnail.image_url}
            alt={thumbnail.style_name}
            className="thumbnail-img"
          />
        ) : thumbnail.status === "failed" ? (
          <span>❌</span>
        ) : (
          <span>⏳</span>
        )}
      </div>
      <div className="thumbnail-info">
        <p className="thumbnail-style">{thumbnail.style_name || "Untitled"}</p>
        <span
          className="thumbnail-status"
          style={{ color: statusColors[thumbnail.status] }}
        >
          {thumbnail.status}
        </span>
        {thumbnail.error_message && (
          <p className="thumbnail-error">{thumbnail.error_message}</p>
        )}
      </div>
    </div>
  )
}
