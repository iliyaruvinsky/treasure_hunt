import React from 'react';
import { Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

interface RiskLevelChartProps {
  data: Record<string, number>;
}

const RiskLevelChart: React.FC<RiskLevelChartProps> = ({ data }) => {
  const chartData = {
    labels: Object.keys(data),
    datasets: [
      {
        label: 'Number of Findings',
        data: Object.values(data),
        backgroundColor: [
          '#dc3545',    // Critical - Red
          '#ffc107',    // High - Amber/Warning
          '#17a2b8',    // Medium - Info/Cyan
          '#28a745',    // Low - Green/Success
        ],
        borderColor: [
          '#dc3545',
          '#ffc107',
          '#17a2b8',
          '#28a745',
        ],
        borderWidth: 0,
        hoverBackgroundColor: [
          '#C41E3A',
          '#e0a800',
          '#138496',
          '#218838',
        ],
        hoverBorderColor: '#ffffff',
        hoverBorderWidth: 2,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false,
      },
      title: {
        display: false,
      },
      tooltip: {
        backgroundColor: '#ffffff',
        titleColor: '#212529',
        bodyColor: '#6c757d',
        borderColor: '#dee2e6',
        borderWidth: 1,
        padding: 12,
        titleFont: {
          family: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
          size: 13,
          weight: '600' as const,
        },
        bodyFont: {
          family: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
          size: 12,
        },
      },
    },
    scales: {
      x: {
        grid: {
          display: false,
        },
        ticks: {
          color: '#6c757d',
          font: {
            family: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
            size: 12,
            weight: '400' as const,
          },
        },
        border: {
          color: '#dee2e6',
        },
      },
      y: {
        beginAtZero: true,
        grid: {
          color: '#f8f9fa',
          lineWidth: 1,
        },
        ticks: {
          stepSize: 1,
          color: '#6c757d',
          font: {
            family: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
            size: 12,
            weight: '400' as const,
          },
        },
        border: {
          color: '#dee2e6',
        },
      },
    },
  };

  return (
    <div style={{ height: '300px' }}>
      <Bar data={chartData} options={options} />
    </div>
  );
};

export default RiskLevelChart;

