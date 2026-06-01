import { Link, useLocation } from "react-router-dom"

const links = [
  { to: "/", label: "Jobs" },
  { to: "/create", label: "New Job" },
]

export default function Navbar() {
  const { pathname } = useLocation()

  return (
    <nav>
      <Link to="/" className="logo">
        ThumbLab
      </Link>
      <div className="nav-links">
        {links.map((link) => (
          <Link
            key={link.to}
            to={link.to}
            className={pathname === link.to ? "active" : ""}
          >
            {link.label}
          </Link>
        ))}
      </div>
    </nav>
  )
}
