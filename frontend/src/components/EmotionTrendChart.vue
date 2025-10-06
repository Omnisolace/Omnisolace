<template>
  <div class="relative h-48">
    <Line :data="chartData" :options="chartOptions" />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js'
import { currentLanguage } from '@/stores/language'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
)

const props = defineProps({
  emotionHistory: {
    type: Array,
    required: true,
    default: () => []
  },
  primaryColor: {
    type: String,
    default: '#fb923c' // 默认橙色
  }
})

const chartData = computed(() => {
  const isZh = currentLanguage.value === 'zh'
  const labels = props.emotionHistory.map((_, index) => 
    isZh ? `第${index + 1}轮` : `Round ${index + 1}`
  )
  const scores = props.emotionHistory.map(e => e.score)

  // 将主题色转换为RGB
  const hexToRgb = (hex) => {
    const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result ? {
      r: parseInt(result[1], 16),
      g: parseInt(result[2], 16),
      b: parseInt(result[3], 16)
    } : { r: 251, g: 146, b: 60 }; // 默认橙色
  };
  
  const rgb = hexToRgb(props.primaryColor);
  const borderColor = `rgba(${rgb.r}, ${rgb.g}, ${rgb.b}, 1)`;
  const gradientStart = `rgba(${rgb.r}, ${rgb.g}, ${rgb.b}, 0.4)`;
  const gradientEnd = `rgba(${rgb.r}, ${rgb.g}, ${rgb.b}, 0)`;

  return {
    labels,
    datasets: [
      {
        label: isZh ? '情绪分数' : 'Emotion Score',
        data: scores,
        fill: true,
        borderColor: borderColor,
        backgroundColor: (context) => {
          const ctx = context.chart.ctx;
          const gradient = ctx.createLinearGradient(0, 0, 0, 200);
          gradient.addColorStop(0, gradientStart);
          gradient.addColorStop(1, gradientEnd);
          return gradient;
        },
        tension: 0.4,
        pointBackgroundColor: borderColor,
        pointBorderColor: '#fff',
        pointHoverBackgroundColor: '#fff',
        pointHoverBorderColor: borderColor,
      }
    ]
  }
})

const chartOptions = computed(() => {
  const isZh = currentLanguage.value === 'zh'
  
  return {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false
      },
      tooltip: {
        enabled: true,
        backgroundColor: '#fff',
        titleColor: '#333',
        bodyColor: '#666',
        borderColor: '#ddd',
        borderWidth: 1,
        callbacks: {
          label: function(context) {
            let label = context.dataset.label || '';
            if (label) {
              label += ': ';
            }
            if (context.parsed.y !== null) {
              label += context.parsed.y.toFixed(1);
            }
            return label;
          }
        }
      }
    },
    scales: {
      y: {
        beginAtZero: false,
        min: -10,
        max: 10,
        title: {
          display: true,
          text: isZh ? '情绪分数' : 'Emotion Score',
          color: '#666',
          font: {
            size: 12,
            weight: '500'
          }
        },
        grid: {
          color: '#f0f0f0',
          drawBorder: false,
        },
        ticks: {
          color: '#999',
          padding: 10,
          stepSize: 5
        }
      },
      x: {
        title: {
          display: true,
          text: isZh ? '对话轮数' : 'Conversation Rounds',
          color: '#666',
          font: {
            size: 12,
            weight: '500'
          }
        },
        grid: {
          display: false
        },
        ticks: {
          color: '#999',
          padding: 10
        }
      }
    }
  }
})
</script>
