import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer
} from "recharts";

export default function DetectionChart({ data = [] }) {
  return (
    <div className="chart-card">
      <div className="section-heading">
        <div>
          <h3>Detection Analytics</h3>
          <p>Vehicle detections over the last 7 days</p>
        </div>

        <span className="chart-badge">LAST 7 DAYS</span>
      </div>

      <div className="chart-container">
        {data.length === 0 ? (
          <div className="chart-empty">
            No detection records available yet.
          </div>
        ) : (
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={data}>
              <CartesianGrid
                stroke="#e9edf2"
                vertical={false}
              />

              <XAxis
                dataKey="day"
                stroke="#929cab"
                axisLine={false}
                tickLine={false}
                fontSize={10}
              />

              <YAxis
                stroke="#929cab"
                axisLine={false}
                tickLine={false}
                fontSize={10}
                allowDecimals={false}
              />

              <Tooltip
                contentStyle={{
                  background: "#ffffff",
                  border: "1px solid #e6e8ec",
                  borderRadius: "5px",
                  color: "#202938",
                  fontSize: "11px"
                }}
              />

              <Area
                type="monotone"
                dataKey="detections"
                stroke="#416b9b"
                strokeWidth={2}
                fill="#416b9b"
                fillOpacity={0.10}
              />
            </AreaChart>
          </ResponsiveContainer>
        )}
      </div>
    </div>
  );
}