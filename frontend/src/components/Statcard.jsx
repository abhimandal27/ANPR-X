import { motion } from "framer-motion";
import { ArrowUpRight } from "lucide-react";

export default function StatCard({
  title,
  value,
  description,
  icon: Icon,
  color,
  delay = 0
}) {
  return (
    <motion.div
      className="stat-card"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.45, delay }}
    >
      <div className="stat-card-top">
        <div className="stat-icon" style={{ color, background: `${color}18` }}>
          <Icon size={22} />
        </div>

        <ArrowUpRight size={18} className="stat-arrow" />
      </div>

      <p className="stat-title">{title}</p>
      <h2>{value}</h2>
      <p className="stat-description">{description}</p>
    </motion.div>
  );
}