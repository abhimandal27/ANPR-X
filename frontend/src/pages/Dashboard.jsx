import { useEffect, useState } from "react";

import {
  ScanLine,
  CarFront,
  Activity,
  ShieldCheck,
  Database,
  Clock3
} from "lucide-react";

import { motion } from "framer-motion";

import StatCard from "../components/StatCard";
import DetectionChart from "../components/DetectionChart";

import {
  getDetectionHistory,
  getHealth
} from "../services/api";


function Dashboard() {
  const [detections, setDetections] = useState([]);
  const [backendStatus, setBackendStatus] = useState("Checking");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    loadDashboard();
  }, []);

  const loadDashboard = async () => {
    try {
      setLoading(true);
      setError("");

      const [historyResponse, healthResponse] = await Promise.all([
        getDetectionHistory(),
        getHealth()
      ]);

      const records = Array.isArray(historyResponse)
        ? historyResponse
        : historyResponse.detections || [];

      setDetections(records);

      setBackendStatus(
        healthResponse.status === "healthy"
          ? "Operational"
          : "Connected"
      );

    } catch (err) {
      console.error("Dashboard loading error:", err);

      setError(
        "Unable to load dashboard data. Check your backend connection."
      );

      setBackendStatus("Offline");

    } finally {
      setLoading(false);
    }
  };

  // Calculate real statistics
  const totalDetections = detections.length;

  const uniqueVehicles = new Set(
    detections.map(item => item.registration_number)
      .filter(Boolean)
  ).size;

  const averageDetection = totalDetections
    ? detections.reduce(
        (sum, item) => sum + Number(item.detection_confidence || 0),
        0
      ) / totalDetections
    : 0;

  const averageOCR = totalDetections
    ? detections.reduce(
        (sum, item) => sum + Number(item.ocr_confidence || 0),
        0
      ) / totalDetections
    : 0;

  // Build chart data from actual detection timestamps
  const chartData = Array.from({ length: 7 }, (_, index) => {
    const date = new Date();
    date.setHours(0, 0, 0, 0);
    date.setDate(date.getDate() - (6 - index));

    const dayRecords = detections.filter(item => {
      const detectionDate = new Date(item.detection_time);

      return (
        !isNaN(detectionDate.getTime()) &&
        detectionDate.toDateString() === date.toDateString()
      );
    });

    return {
      day: date.toLocaleDateString("en-IN", {
        weekday: "short"
      }),
      detections: dayRecords.length
    };
  });

  const formatPercentage = value =>
    `${(value * 100).toFixed(1)}%`;

  const formatTime = value => {
    if (!value) return "—";

    const date = new Date(value);

    if (isNaN(date.getTime())) return value;

    return date.toLocaleString("en-IN", {
      day: "2-digit",
      month: "short",
      hour: "2-digit",
      minute: "2-digit"
    });
  };

  return (
    <motion.div
      className="dashboard-page"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.3 }}
    >

      {/* Welcome Section */}

      <section className="welcome-section">
        <div>
          <p className="welcome-label">
            VEHICLE MANAGEMENT SYSTEM
          </p>

          <h2>System Overview</h2>

          <p className="welcome-description">
            Monitor vehicle detections and recognition performance.
          </p>
        </div>

        <div className="system-indicator">
          <span className="status-dot"></span>
          {backendStatus.toUpperCase()}
        </div>
      </section>


      {/* Error Message */}

      {error && (
        <div className="dashboard-error">
          {error}
          <button onClick={loadDashboard}>
            Retry
          </button>
        </div>
      )}


      {/* Statistics */}

      <section className="stats-grid">

        <StatCard
          title="Total Detections"
          value={loading ? "..." : totalDetections.toLocaleString()}
          description="Recorded detection entries"
          icon={ScanLine}
          color="#416b9b"
        />

        <StatCard
          title="Unique Vehicles"
          value={loading ? "..." : uniqueVehicles.toLocaleString()}
          description="Distinct registration numbers"
          icon={CarFront}
          color="#398266"
        />

        <StatCard
          title="Avg. Detection Confidence"
          value={loading ? "..." : formatPercentage(averageDetection)}
          description="YOLO detection confidence"
          icon={Activity}
          color="#a47b32"
        />

        <StatCard
          title="Avg. OCR Confidence"
          value={loading ? "..." : formatPercentage(averageOCR)}
          description="Text recognition confidence"
          icon={ShieldCheck}
          color="#7566a0"
        />

      </section>


      {/* Analytics */}

      <section className="dashboard-grid">

        <DetectionChart data={chartData} />

        <div className="activity-card">

          <div className="section-heading">
            <div>
              <h3>System Status</h3>
              <p>Backend service information</p>
            </div>

            <Activity size={19} />
          </div>

          <div className="activity-item">
            <span className="activity-icon blue">
              <ScanLine size={17} />
            </span>

            <div>
              <h4>ANPR Engine</h4>
              <p>Number plate detection service</p>
            </div>

            <span className="activity-status">
              {backendStatus}
            </span>
          </div>

          <div className="activity-item">
            <span className="activity-icon green">
              <Database size={17} />
            </span>

            <div>
              <h4>Detection Database</h4>
              <p>SQLite detection records</p>
            </div>

            <span className="activity-status">
              {backendStatus === "Offline" ? "Offline" : "Connected"}
            </span>
          </div>

          <div className="activity-item">
            <span className="activity-icon purple">
              <ShieldCheck size={17} />
            </span>

            <div>
              <h4>OCR Engine</h4>
              <p>Plate text recognition</p>
            </div>

            <span className="activity-status">
              {backendStatus}
            </span>
          </div>

          <div className="activity-footer">
            <Clock3 size={14} />
            <span>
              {loading ? "Loading system information" : "Connected to ANPR-X API"}
            </span>
          </div>

        </div>

      </section>


      {/* Recent Detections */}

      <section className="recent-card">

        <div className="section-heading">
          <div>
            <h3>Recent Detections</h3>
            <p>Latest records from the detection database</p>
          </div>

          <button
            className="view-all-button"
            onClick={loadDashboard}
          >
            Refresh
          </button>
        </div>

        <div className="table-wrapper">

          <table>

            <thead>
              <tr>
                <th>REGISTRATION NUMBER</th>
                <th>DETECTION TIME</th>
                <th>DETECTION CONFIDENCE</th>
                <th>OCR CONFIDENCE</th>
                <th>STATUS</th>
              </tr>
            </thead>

            <tbody>

              {loading ? (
                <tr>
                  <td colSpan="5">Loading detection records...</td>
                </tr>
              ) : detections.length === 0 ? (
                <tr>
                  <td colSpan="5">
                    No detection records found. Run your first ANPR scan.
                  </td>
                </tr>
              ) : (
                detections.slice(0, 8).map((item, index) => (
                  <tr key={item.id || index}>

                    <td className="plate-number">
                      {item.registration_number || "Unknown"}
                    </td>

                    <td>
                      {formatTime(item.detection_time)}
                    </td>

                    <td>
                      {formatPercentage(
                        Number(item.detection_confidence || 0)
                      )}
                    </td>

                    <td>
                      {formatPercentage(
                        Number(item.ocr_confidence || 0)
                      )}
                    </td>

                    <td>
                      <span className="table-status verified">
                        Recorded
                      </span>
                    </td>

                  </tr>
                ))
              )}

            </tbody>

          </table>

        </div>

      </section>

    </motion.div>
  );
}

export default Dashboard;