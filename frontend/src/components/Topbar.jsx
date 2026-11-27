import { Bell, Search, Command } from "lucide-react";

export default function Topbar({ title, subtitle }) {
  return (
    <header className="topbar">
      <div className="page-heading">
        <h1>{title}</h1>
        <p>{subtitle}</p>
      </div>

      <div className="topbar-actions">
        <div className="search-box">
          <Search size={18} />
          <input placeholder="Search anything..." />
          <span><Command size={12} /> K</span>
        </div>

        <button className="icon-button">
          <Bell size={19} />
          <span className="notification-dot" />
        </button>

        <div className="profile-avatar">PS</div>
      </div>
    </header>
  );
}