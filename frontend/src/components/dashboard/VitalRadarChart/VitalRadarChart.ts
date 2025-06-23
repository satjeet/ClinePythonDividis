import { computed } from 'vue';
import { use } from 'echarts/core';
import { CanvasRenderer } from 'echarts/renderers';
import { RadarChart } from 'echarts/charts';
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  RadarComponent
} from 'echarts/components';

use([
  CanvasRenderer,
  RadarChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  RadarComponent
]);

const labels = [
  'Salud',           // 12:00
  'Relaciones',      // 1:30
  'Emocionalidad',   // 3:00
  'Calidad de Vida', // 4:30
  'Finanzas',        // 6:00
  'Carrera',         // 7:30
  'Intelecto',       // 9:00
  'Personalidad'     // 10:30
];

export function useChartOptions(props: { values?: number[] }) {
  const chartValues = computed(() => props.values && props.values.length === 8 ? props.values : [80, 60, 70, 30, 40, 50, 20, 60]);

  const chartOption = computed(() => {
    // Responsive: reducir el radius en mobile
    const isMobile = typeof window !== 'undefined' && window.innerWidth < 640;
    const radarRadius = isMobile ? '52%' : '70%';
    const radarCenter = ['50%', '50%'];

    return {
      backgroundColor: '#090f20', // Establece el color de fondo del gráfico
      tooltip: {},
      radar: {
        indicator: labels.map(label => ({ name: label, max: 100 })),
        radius: radarRadius, // Responsive
        center: radarCenter, // Responsive
        axisName: {
          color: '#fff', // Color blanco para los labels de los ejes
          fontSize: isMobile ? 12 : 24, // Más pequeño en mobile
          fontFamily: 'var(--theme-font)',
          formatter: function (value: string) {
            if (value === 'Emocionalidad') {
              return value;
            }
            return value;
          },
          rich: {
            a: {
              // Estilos específicos para "Emocionalidad" si se necesita un ajuste fino
            }
          }
        },
        axisLine: {
          lineStyle: {
            color: '#1e293b' // gray-800
          }
        },
        splitLine: {
          lineStyle: {
            color: '#1e293b' // gray-800
          }
        },
        splitArea: {
          areaStyle: {
            color: ['rgba(255, 255, 255, 0.05)', 'rgba(255, 255, 255, 0.02)'] // Colores de las áreas concéntricas, más sutiles
          }
        }
      },
      series: [
        {
          name: 'Progreso Vital',
          type: 'radar',
          data: [
            {
              value: chartValues.value,
              name: 'Progreso',
              areaStyle: {
                opacity: 0.5,
                color: '#38bdf8' // sky-400
              },
              lineStyle: {
                color: '#38bdf8' // sky-400
              }
            }
          ]
        }
      ]
    };
  });

  return { chartOption };
}
