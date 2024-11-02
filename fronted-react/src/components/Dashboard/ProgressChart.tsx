import React from "react";
import { Pie } from "react-chartjs-2";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from "chart.js";

ChartJS.register(ArcElement, Tooltip, Legend);

const pieData = {
  labels: ["Completed", "Uncompleted", "Missed Deadline"],
  datasets: [
    {
      data: [60, 30, 10],
      backgroundColor: ["#34D399", "#FBBF24", "#EF4444"],
    },
  ],
};

const chartOptions = {
  plugins: {
    legend: {
      display: true,
      position: "bottom" as const,
      labels: {
        usePointStyle: true,
        padding: 20,
        font: {
          size: 14,
        },
        color: "#ffffff",
      },
    },
  },
};

const ProgressChart: React.FC = () => {
  return (
    <div className="flex-1 bg-gray-900 p-6 rounded-2xl shadow-lg flex items-center justify-center">
      <Pie data={pieData} options={chartOptions} />
    </div>
  );
};

export default ProgressChart;
