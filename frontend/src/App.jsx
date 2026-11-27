import { useState } from "react";
import { AnimatePresence, motion } from "framer-motion";

import Sidebar from "./components/Sidebar";
import Topbar from "./components/Topbar";
import Dashboard from "./pages/Dashboard";

import {
  ScanLine,
  CarFront,
  Receipt,
  History
} from "lucide-react";

import "./App.css";

const pageDetails = {
  dashboard: {
    title: "Dashboard",
    subtitle: "Welcome to your vehicle intelligence control centre."
  },
  scanner: {
    title: "ANPR Scanner",
    subtitle: "Detect and recognize vehicle registration plates."
  },
  vehicles: {
    title: "Vehicle Management",
    subtitle: "Explore registered vehicle information."
  },
  challans: {
    title: "Challan Records",
    subtitle: "Monitor traffic violations and challan records."
  },
  history: {
    title: "Detection History",
    subtitle: "Review previously detected vehicles."
  }
};

function PlaceholderPage({ page }) {
  const pageConfig = {
    scanner: {
      icon: ScanLine,
      heading: "ANPR Scanner",
      description: "Your intelligent number plate scanning workspace is coming next."
    },
    vehicles: {
      icon: CarFront,
      heading: "Vehicle Management",
      description: "Vehicle profiles and registration records will appear here."
    },
    challans: {
      icon: Receipt,
      heading: "Challan Management",
      description: "Traffic violation records and challan history will appear here."
    },
    history: {
      icon: History,
      heading: "Detection History",
      description: "Your previous ANPR detection records will appear here."
    }
  };

  const config = pageConfig[page];
  const Icon = config.icon;

  return (
    <motion.div
      className="placeholder-page"
      initial={{ opacity: 0, y: 15 }}
      animate={{ opacity: 1, y: 0 }}
    >
      <div className="placeholder-icon">
        <Icon size={36} />
      </div>

      <h2>{config.heading}</h2>
      <p>{config.description}</p>

      <span className="coming-soon">MODULE UNDER DEVELOPMENT</span>
    </motion.div>
  );
}

function App() {
  const [activePage, setActivePage] = useState("dashboard");

  const currentPage = pageDetails[activePage];

  return (
    <div className="app-layout">
      <Sidebar
        activePage={activePage}
        setActivePage={setActivePage}
      />

      <main className="main-content">
        <Topbar
          title={currentPage.title}
          subtitle={currentPage.subtitle}
        />

        <div className="page-content">
          <AnimatePresence mode="wait">
            <motion.div
              key={activePage}
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -8 }}
              transition={{ duration: 0.2 }}
            >
              {activePage === "dashboard" ? (
                <Dashboard />
              ) : (
                <PlaceholderPage page={activePage} />
              )}
            </motion.div>
          </AnimatePresence>
        </div>
      </main>
    </div>
  );
}

export default App;