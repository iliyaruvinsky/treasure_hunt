import React from 'react';
import { Doughnut } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(ArcElement, Tooltip, Legend);

interface FocusAreaChartProps {
  data: Record<string, number>;
}

const FocusAreaChart: React.FC<FocusAreaChartProps> = ({ data }) => {
  // Skywind professional color palette
  const colors = [
    '#C41E3A',    // Skywind Red - Business Protection
    '#dc3545',    // Red - Business Control
    '#ffc107',    // Yellow/Amber - Access Governance
    '#17a2b8',    // Cyan/Info - Technical Control
    '#28a745',    // Green - Jobs Control
    '#6c757d',    // Gray - S/4HANA Excellence
  ];

  const chartData = {
    labels: Object.keys(data).map(key => {
      const names: Record<string, string> = {
        'BUSINESS_PROTECTION': 'Business Protection',
        'BUSINESS_CONTROL': 'Business Control',
        'ACCESS_GOVERNANCE': 'Access Governance',
        'TECHNICAL_CONTROL': 'Technical Control',
        'JOBS_CONTROL': 'Jobs Control',
        'S4HANA_EXCELLENCE': 'S/4HANA Excellence',
      };
      return names[key] || key;
    }),
    datasets: [
      {
        data: Object.values(data),
        backgroundColor: colors.slice(0, Object.keys(data).length),
        borderColor: '#ffffff',
        borderWidth: 2,
        hoverBorderColor: '#C41E3A',
        hoverBorderWidth: 3,
        hoverOffset: 10,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'right' as const,
        labels: {
          color: '#212529',
          font: {
            family: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
            size: 12,
            weight: '500' as const,
          },
          padding: 15,
          usePointStyle: true,
          pointStyle: 'circle',
        },
      },
      tooltip: {
        backgroundColor: '#ffffff',
        titleColor: '#212529',
        bodyColor: '#6c757d',
        borderColor: '#dee2e6',
        borderWidth: 1,
        padding: 12,
        displayColors: true,
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
            const label = context.label || '';
            const value = context.parsed || 0;
            const total = context.dataset.data.reduce((a: number, b: number) => a + b, 0);
            const percentage = ((value / total) * 100).toFixed(1);
            return ` ${label}: ${value} findings (${percentage}%)`;
          },
        },
      },
    },
  };

  return (
    <div style={{ height: '400px' }}>
      <Doughnut data={chartData} options={options} />
    </div>
  );
};

export default FocusAreaChart;

