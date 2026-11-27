import {
  LayoutDashboard,
  ScanLine,
  CarFront,
  Receipt,
  History,
  Settings,
  ShieldCheck
} from "lucide-react";

const menuItems = [
  { name: "Dashboard", icon: LayoutDashboard, id: "dashboard" },
  { name: "ANPR Scanner", icon: ScanLine, id: "scanner" },
  { name: "Vehicles", icon: CarFront, id: "vehicles" },
  { name: "Challan Records", icon: Receipt, id: "challans" },
  { name: "Detection History", icon: History, id: "history" }
];

export default function Sidebar({ activePage, setActivePage }) {
  return (
    <aside className="sidebar">

      <div className="brand">
        <div className="brand-icon">
          <ShieldCheck size={25} />
        </div>

        <div>
          <h2>ANPR<span>-X</span></h2>
          <p>INTELLIGENCE SYSTEM</p>
        </div>
      </div>

      <div className="menu-label">MAIN MENU</div>

      <nav>
        {menuItems.map((item) => {
          const Icon = item.icon;

          return (
            <button
              key={item.id}
              className={`nav-item ${
                activePage === item.id ? "active" : ""
              }`}
              onClick={() => setActivePage(item.id)}
            >
              <Icon size={19} />
              <span>{item.name}</span>
            </button>
          );
        })}
      </nav>

      <div className="sidebar-bottom">
        <button className="nav-item">
          <Settings size={19} />
          <span>Settings</span>
        </button>

        <div className="system-status">
          <span className="status-dot"></span>
          SYSTEM OPERATIONAL
        </div>

        <p className="sidebar-version">ANPR-X v1.0.0</p>
      </div>

    </aside>
  );
}