/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // 动态主题色彩 - 通过CSS变量实现
        primary: {
          50: 'var(--color-primary-50, #FFF8F0)',
          100: 'var(--color-primary-100, #FFE8CC)',
          500: 'var(--color-primary, #FFA84A)',
          600: 'var(--color-primary-600, #E67E22)',
        },
        secondary: 'var(--color-secondary, #FFD29D)',
        accent: 'var(--color-accent, #E67E22)',
        background: 'var(--color-background, #FFF8F0)',
        'text-theme': 'var(--color-text, #664E33)',
        
        // 暖阳橘主题（默认）
        'warm-orange': {
          50: '#FFF8F0',
          100: '#FFE8CC',
          500: '#FFA84A',
          600: '#E67E22',
        },
        
        // 柔粉棕主题
        'soft-pink-brown': {
          50: '#FCF7F4',
          100: '#F3D9C6',
          500: '#D4B499',
          600: '#A67C52',
        },
        
        // 琥珀黄主题
        'amber-yellow': {
          50: '#FFFDF5',
          100: '#FFE8A3',
          500: '#F5C745',
          600: '#DBA82C',
        },
        
        // 焦糖棕主题
        'caramel-brown': {
          50: '#F7F1E7',
          100: '#E8C39E',
          500: '#C18A50',
          600: '#8B5A2B',
        },
        
        // 樱花粉主题
        'cherry-pink': {
          50: '#FFFBFC',
          100: '#FFE0E9',
          500: '#FFB7C5',
          600: '#E68598',
        },
        
        // 情绪状态色彩
        emotion: {
          happy: '#10b981',
          neutral: '#6b7280',
          sad: '#3b82f6',
          anxious: '#f59e0b',
          angry: '#ef4444',
        }
      },
      fontSize: {
        // 老年模式大字体
        'elder-sm': ['16px', '24px'],
        'elder-base': ['18px', '28px'],
        'elder-lg': ['20px', '32px'],
        'elder-xl': ['24px', '36px'],
        'elder-2xl': ['28px', '40px'],
      },
      spacing: {
        // 老年模式大按钮
        '18': '4.5rem', // 72px
        '20': '5rem',   // 80px
      }
    },
  },
  plugins: [],
}
