import React from 'react';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

interface MoneyLossChartProps {
  data: Array<{ date: string; amount: number }>;
}

const MoneyLossChart: React.FC<MoneyLossChartProps> = ({ data }) => {
  const chartData = {
    labels: data.map(d => new Date(d.date).toLocaleDateString()),
    datasets: [
      {
        label: 'Estimated Financial Exposure',
        data: data.map(d => d.amount),
        borderColor: '#C41E3A',
        backgroundColor: 'rgba(196, 30, 58, 0.1)',
        pointBackgroundColor: '#C41E3A',
        pointBorderColor: '#ffffff',
        pointBorderWidth: 2,
        pointRadius: 4,
        pointHoverRadius: 7,
        pointHoverBackgroundColor: '#C41E3A',
        pointHoverBorderColor: '#ffffff',
        pointHoverBorderWidth: 3,
        tension: 0.4,
        fill: true,
        borderWidth: 2,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: true,
        labels: {
          color: '#212529',
          font: {
            family: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
            size: 12,
            weight: '500' as const,
          },
          padding: 15,
          usePointStyle: true,
        },
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
        callbacks: {
          label: (context: any) => {
            return ` Financial Exposure: $${context.parsed.y.toLocaleString()}`;
          },
        },
      },
    },
    scales: {
      x: {
        grid: {
          color: '#f8f9fa',
          lineWidth: 1,
        },
        ticks: {
          color: '#6c757d',
          font: {
            family: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
            size: 11,
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
          color: '#6c757d',
          font: {
            family: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
            size: 11,
            weight: '400' as const,
          },
          callback: (value: any) => `$${value.toLocaleString()}`,
        },
        border: {
          color: '#dee2e6',
        },
      },
    },
  };

  return (
    <div style={{ height: '300px' }}>
      <Line data={chartData} options={options} />
    </div>
  );
};

export default MoneyLossChart;

